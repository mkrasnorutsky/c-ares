#include <ares.h>
#include <stdio.h>
int main(void) {
    /* A synthetic DNS A response for example.test -> 192.0.2.1. No network requests. */
    static const unsigned char packet[]={
        0x12,0x34,0x81,0x80,0,1,0,1,0,0,0,0,
        7,'e','x','a','m','p','l','e',4,'t','e','s','t',0,0,1,0,1,
        0xc0,0x0c,0,1,0,1,0,0,0,60,0,4,192,0,2,1};
    ares_dns_record_t *record=NULL,*copy=NULL;
    unsigned char *wire=NULL; size_t wire_size=0; int version=0;
    if(ares_library_init(ARES_LIB_INIT_ALL)!=ARES_SUCCESS)return 1;
    (void)ares_version(&version);
    if(version!=ARES_VERSION)return 2;
    if(ares_dns_parse(packet,sizeof(packet),0,&record)!=ARES_SUCCESS)return 3;
    if(ares_dns_record_get_id(record)!=0x1234 || ares_dns_record_rr_cnt(record,ARES_SECTION_ANSWER)!=1)return 4;
    if(ares_dns_write(record,&wire,&wire_size)!=ARES_SUCCESS)return 5;
    if(ares_dns_parse(wire,wire_size,0,&copy)!=ARES_SUCCESS)return 6;
    if(ares_dns_record_get_id(copy)!=0x1234 || ares_dns_record_rr_cnt(copy,ARES_SECTION_ANSWER)!=1)return 7;
    ares_dns_record_destroy(copy);ares_dns_record_destroy(record);ares_free_string(wire);ares_library_cleanup();
    puts("PASS: DNS parse/write/parse round-trip, initialization and header/library version match");
    return 0;
}

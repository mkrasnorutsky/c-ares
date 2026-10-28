#include <ares.h>
#include <stdio.h>
#include <string.h>
#include <netinet/in.h>
static int valid_answer(ares_dns_record_t *record) {
    const unsigned char expected[]={192,0,2,1};
    const char *name=NULL; ares_dns_rec_type_t type; ares_dns_class_t dnsclass;
    const ares_dns_rr_t *rr; const struct in_addr *address;
    if(ares_dns_record_get_id(record)!=0x1234 || ares_dns_record_rr_cnt(record,ARES_SECTION_ANSWER)!=1)return 0;
    if(ares_dns_record_query_get(record,0,&name,&type,&dnsclass)!=ARES_SUCCESS || !name || strcmp(name,"example.test") || type!=ARES_REC_TYPE_A || dnsclass!=ARES_CLASS_IN)return 0;
    rr=ares_dns_record_rr_get(record,ARES_SECTION_ANSWER,0);
    if(!rr || ares_dns_rr_get_type(rr)!=ARES_REC_TYPE_A)return 0;
    address=ares_dns_rr_get_addr(rr,ARES_RR_A_ADDR);
    return address && !memcmp(&address->s_addr,expected,sizeof(expected));
}
int main(void) {
    /* A synthetic DNS A response for example.test -> 192.0.2.1. No network requests. */
    static const unsigned char packet[]={
        0x12,0x34,0x81,0x80,0,1,0,1,0,0,0,0,
        7,'e','x','a','m','p','l','e',4,'t','e','s','t',0,0,1,0,1,
        0xc0,0x0c,0,1,0,1,0,0,0,60,0,4,192,0,2,1};
    ares_dns_record_t *record=NULL,*copy=NULL;
    unsigned char *wire=NULL; size_t wire_size=0; int version=0; ares_channel_t *channel=NULL;
    if(ares_library_init(ARES_LIB_INIT_ALL)!=ARES_SUCCESS)return 1;
    (void)ares_version(&version);
    if(version!=ARES_VERSION)return 2;
    if(ares_init_options(&channel,NULL,0)!=ARES_SUCCESS)return 8;
    ares_destroy(channel);
    if(ares_dns_parse(packet,sizeof(packet),0,&record)!=ARES_SUCCESS)return 3;
    if(!valid_answer(record))return 4;
    if(ares_dns_write(record,&wire,&wire_size)!=ARES_SUCCESS)return 5;
    if(ares_dns_parse(wire,wire_size,0,&copy)!=ARES_SUCCESS)return 6;
    if(!valid_answer(copy))return 7;
    ares_dns_record_destroy(copy);ares_dns_record_destroy(record);ares_free_string(wire);ares_library_cleanup();
    puts("PASS: DNS parse/write/parse round-trip, initialization and header/library version match");
    return 0;
}

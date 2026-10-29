#!/usr/bin/env python3
"""Link all iOS architectures and run an offline native DNS parser round-trip."""
from pathlib import Path
import plistlib,subprocess,tempfile
from build_xcframework import ROOT,configure
artifact=WORK/'dist/CAres.xcframework';info=plistlib.loads((artifact/'Info.plist').read_bytes());assert len(info['AvailableLibraries'])==2
for entry in info['AvailableLibraries']:
    sim=entry.get('SupportedPlatformVariant')=='simulator'
    assert entry['SupportedPlatform']=='ios'
    assert set(entry['SupportedArchitectures'])==({'arm64','x86_64'} if sim else {'arm64'})
    folder=artifact/entry['LibraryIdentifier'];archive=folder/entry['LibraryPath'];headers=folder/entry['HeadersPath']
    subprocess.run(['lipo',str(archive),'-verify_arch',*entry['SupportedArchitectures']],check=True)
    sdk=subprocess.check_output(['xcrun','--sdk','iphonesimulator' if sim else 'iphoneos','--show-sdk-path'],text=True).strip()
    for arch in entry['SupportedArchitectures']:
        triple=arch+'-apple-ios18.0'+('-simulator' if sim else '')
        with tempfile.TemporaryDirectory(prefix='cares-client-') as directory:
            subprocess.run(['xcrun','clang','-target',triple,'-isysroot',sdk,'-DCARES_STATICLIB','-fmodules','-fmodules-cache-path='+directory+'/modules','-I'+str(headers),str(ROOT/'apple/scripts/dns_smoke.c'),str(archive),'-lresolv','-o',directory+'/client'],check=True)
print('PASS: APIs link on arm64 device and arm64/x86_64 Simulator',flush=True)
build=WORK/'out/native-validation';prefix=build/'install';configure(build,prefix)
subprocess.run(['xcrun','clang','-DCARES_STATICLIB','-I'+str(prefix/'include'),str(ROOT/'apple/scripts/dns_smoke.c'),str(prefix/'lib/libcares.a'),'-lresolv','-o',str(build/'dns_smoke')],check=True)
subprocess.run([str(build/'dns_smoke')],check=True)
import os
WORK=Path(os.environ.get("APPLE_BUILD_ROOT", str(ROOT))).expanduser().resolve()

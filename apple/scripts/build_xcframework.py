#!/usr/bin/env python3
"""Build a static c-ares XCFramework for arm64 iPhone and arm64/x86_64 Simulator."""
from pathlib import Path
import argparse,json,shutil,subprocess
ROOT=Path(__file__).resolve().parents[2]
OPTIONS=['-DCARES_STATIC=ON','-DCARES_SHARED=OFF','-DCARES_INSTALL=ON','-DCARES_BUILD_TESTS=OFF','-DCARES_BUILD_CONTAINER_TESTS=OFF','-DCARES_BUILD_TOOLS=OFF','-DCARES_THREADS=ON']
def run(*args):
    print('+',' '.join(map(str,args)),flush=True);return subprocess.run(list(map(str,args)),check=True)
def configure(build,prefix,sdk=None,arch=None,jobs=6):
    flags=OPTIONS+['-DCMAKE_BUILD_TYPE=Release','-DCMAKE_INSTALL_PREFIX='+str(prefix)]
    if sdk:flags+=['-DCMAKE_SYSTEM_NAME=iOS','-DCMAKE_OSX_SYSROOT='+sdk,'-DCMAKE_OSX_ARCHITECTURES='+arch,'-DCMAKE_OSX_DEPLOYMENT_TARGET=18.0']
    run('cmake','-S',ROOT,'-B',build,*flags)
    run('cmake','--build',build,'--parallel',jobs)
    run('cmake','--install',build)
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--jobs',type=int,default=6);a=p.parse_args();built={}
    configurations=[('ios-arm64','iphoneos','arm64'),('simulator-arm64','iphonesimulator','arm64'),('simulator-x86_64','iphonesimulator','x86_64')]
    for label,sdk,arch in configurations:
        build=ROOT/'out/apple'/label;prefix=build/'install';configure(build,prefix,sdk,arch,a.jobs);built[label]=prefix
    out=ROOT/'dist';out.mkdir(exist_ok=True);staging=out/'staging'
    if staging.exists():shutil.rmtree(staging)
    staging.mkdir();universal=staging/'libcares.a'
    run('lipo','-create',built['simulator-arm64']/'lib/libcares.a',built['simulator-x86_64']/'lib/libcares.a','-output',universal)
    artifact=out/'CAres.xcframework'
    if artifact.exists():shutil.rmtree(artifact)
    command=['xcodebuild','-create-xcframework']
    # ares_build.h describes the ABI and may vary across architectures.
    # Use the actual device header set for device and Simulator's header set for Simulator.
    for label,archive in [('ios-arm64',built['ios-arm64']/'lib/libcares.a'),('simulator-arm64',universal)]:
        headers=staging/label/'Headers';shutil.copytree(built[label]/'include',headers)
        (headers/'module.modulemap').write_text('module CCAres {\n header "ares.h"\n export *\n}\n')
        command+=['-library',str(archive),'-headers',str(headers)]
    command+=['-output',str(artifact)];run(*command)
    notices=artifact/'Licenses';notices.mkdir();shutil.copy2(ROOT/'LICENSE.md',notices/'LICENSE.md')
    if (ROOT/'LICENSES').is_dir():shutil.copytree(ROOT/'LICENSES',notices/'LICENSES')
    manifest={'source_revision':subprocess.check_output(['git','-C',str(ROOT),'rev-parse','HEAD'],text=True).strip(),'upstream_revision':'4c6046531646906e9a493d542bd7f1f63da9650e','minimum_ios':'18.0','linkage':'static','slices':[x[0] for x in configurations],'system_libraries':['resolv'],'cmake_options':OPTIONS}
    (out/'build-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print('Created',artifact)
if __name__=='__main__':main()

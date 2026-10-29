# c-ares for iOS and Swift Package Manager

The complete tracked c-ares sources and upstream history are preserved at OneClickPilot's pinned revision `4c6046531646906e9a493d542bd7f1f63da9650e`. This package supplies SimGear's asynchronous DNS dependency.

## Use the package

Add `https://github.com/mkrasnorutsky/c-ares.git` in Xcode, select version **0.1.0** or later, and add the **CAres** product. It integrates a checksum-verified static XCFramework for **arm64 iPhone, arm64 Simulator and x86_64 Simulator**, with minimum iOS **18.0**. The binary module is **CCAres**. Public headers keep the standard `<ares.h>` interface; the wrapper header is `CAresSPM.h`.

[Release 0.1.0](https://github.com/mkrasnorutsky/c-ares/releases/tag/0.1.0) contains the XCFramework ZIP, checksum and build manifest. SPM integrates the compiled library; it does not run CMake during package resolution. The wrapper declares the system `resolv` link dependency and static-library define. Follow c-ares' normal library/channel initialization and cleanup APIs when using the resolver.

## Build

Requirements: macOS, Xcode with iPhoneOS/iPhoneSimulator SDKs, CMake, Python 3 and Git. No extra library downloads or signing identity are required.

```sh
git clone https://github.com/mkrasnorutsky/c-ares.git
cd c-ares
python3 apple/scripts/build_xcframework.py --jobs 6
python3 apple/scripts/validate_xcframework.py
```

CMake builds each architecture independently. Lipo combines only the two Simulator archives, then Xcode packages them with the device archive as `dist/CAres.xcframework`. Public/generated headers, a Clang module map and upstream license notices are included. Thread support stays enabled; CLI tools and upstream/container test executables are disabled in distribution builds.

Validation links the public DNS APIs for each iOS architecture. It then builds a separate native macOS library and executes an offline DNS response parse/write/parse round-trip, checking query name/type/class, answer address, record counts, library/channel initialization and header/library version. The fixture uses `example.test` and `192.0.2.1`; it makes no live DNS request. This validates source behavior on the host, not DNS connectivity on a physical iPhone or Simulator.

A manual GitHub Actions workflow runs the same builds and checks. Use `--jobs N` to choose parallelism. To consume locally rebuilt artifacts, copy `apple/Package.local.swift` to the root `Package.swift` and add this folder as a local package.

## Release packaging

```sh
python3 apple/scripts/package_release.py --tag 0.2.0
```

Upload the generated ZIP and checksums to the matching GitHub release, then commit `dist/Package.swift` as the root manifest at the release revision. Published archive contents and checksums remain immutable. Original `LICENSE.md` and `LICENSES` notices are retained in the repository and XCFramework.

## Xcode header layout (0.1.1)

Binary module maps live under a module-specific header subdirectory, avoiding duplicate `include/module.modulemap` outputs when Xcode processes several static XCFrameworks together. The library bytes and public include paths are unchanged. Set `APPLE_BUILD_ROOT` to keep `out/` and `dist/` outside the checkout.

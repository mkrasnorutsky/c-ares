// swift-tools-version: 5.9
import PackageDescription
let package = Package(name: "CAres", platforms: [.iOS("18.0")],
    products: [.library(name: "CAres", targets: ["CAres"])],
    targets: [
        .binaryTarget(name: "CCAres", url: "https://github.com/mkrasnorutsky/c-ares/releases/download/0.1.0/CAres.xcframework.zip", checksum: "6a02c72d3b0756a8ce376823dfabcd2798dc5f00ab9c2fc54e6be3991e548f45"),
        .target(name: "CAres", dependencies: ["CCAres"], path: "apple/SPM", publicHeadersPath: "include",
                cSettings: [.define("CARES_STATICLIB")], linkerSettings: [.linkedLibrary("resolv")])
    ])

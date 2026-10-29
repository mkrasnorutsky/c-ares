// swift-tools-version: 5.9
import PackageDescription
let package = Package(name: "CAres", platforms: [.iOS("18.0")],
    products: [.library(name: "CAres", targets: ["CAres"])],
    targets: [
        .binaryTarget(name: "CCAres", url: "https://github.com/mkrasnorutsky/c-ares/releases/download/0.1.1/CAres.xcframework.zip", checksum: "804ebc74af460f870c8d1056725061bb5838471739697324da9a7175c75dfa64"),
        .target(name: "CAres", dependencies: ["CCAres"], path: "apple/SPM", publicHeadersPath: "include",
                cSettings: [.define("CARES_STATICLIB")], linkerSettings: [.linkedLibrary("resolv")])
    ])

// swift-tools-version: 5.9
import PackageDescription
let package = Package(name: "CAres", platforms: [.iOS("18.0")],
    products: [.library(name: "CAres", targets: ["CAres"])],
    targets: [
        .binaryTarget(name: "CCAres", url: "https://github.com/mkrasnorutsky/c-ares/releases/download/0.1.1/CAres.xcframework.zip", checksum: "8773c2981fc8e1b84e40f64d7e7f6fe57a165bc31216c9af427e93c2e7146958"),
        .target(name: "CAres", dependencies: ["CCAres"], path: "apple/SPM", publicHeadersPath: "include",
                cSettings: [.define("CARES_STATICLIB")], linkerSettings: [.linkedLibrary("resolv")])
    ])

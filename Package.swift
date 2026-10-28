// swift-tools-version: 5.9
import PackageDescription
let package = Package(name: "CAres", platforms: [.iOS("18.0")],
    products: [.library(name: "CAres", targets: ["CAres"])],
    targets: [
        .binaryTarget(name: "CCAres", path: "dist/CAres.xcframework"),
        .target(name: "CAres", dependencies: ["CCAres"], path: "apple/SPM", publicHeadersPath: "include",
                cSettings: [.define("CARES_STATICLIB")], linkerSettings: [.linkedLibrary("resolv")])
    ])

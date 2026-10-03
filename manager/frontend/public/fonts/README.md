# Report export fonts

Embedded (as subsets) in generated PDF reports. This directory is copied into the
production standalone image as well as local and server builds.

## IBM Plex Sans and IBM Plex Mono

The report's text and code faces. WOFF files from the official npm packages
`@ibm/plex-sans` 1.1.0 and `@ibm/plex-mono` 2.5.0 (`fonts/complete/woff`).
Licensed under the SIL Open Font License 1.1, see `IBM-Plex-OFL.txt`.

| File | SHA-256 |
| --- | --- |
| `IBMPlexSans-Regular.woff` | `b731cf56514a4bd711ab2f9acf641f9311707f4386772eb306d25c2b29b73b1a` |
| `IBMPlexSans-Italic.woff` | `ed06e0a2cfa973492c7ee61e5f1bf3be7db4d3d5c1551c889ec458ba2972db99` |
| `IBMPlexSans-Medium.woff` | `2b6a04d0f593ad57740e0f51c1bf0b1e3f05f27209c7ca1697a0a72973150f3f` |
| `IBMPlexSans-SemiBold.woff` | `fff45f420f0d026b4a39f99b3bfc47dfc06561c598c8db825cfce5fd706bda7a` |
| `IBMPlexSans-Bold.woff` | `5c8bcd6be12df67acd529819b92f36febeff4df059a9603c4ecd578f01cf4062` |
| `IBMPlexMono-Regular.woff` | `3a0d6e1587e8dc784be5a75e1c55b1a5533919b04072a29c750bb29cfe4a4b74` |
| `IBMPlexMono-Medium.woff` | `fa311409acb7ee09c9c1564e7ac90306199eb1632bf571a082cf3a1db5f6be98` |

## GNU Unifont (fallback)

`unifont-17.0.05.otf` is GNU Unifont 17.0.05, downloaded from the
[official Unifoundry release](https://unifoundry.com/pub/unifont/unifont-17.0.05/font-builds/unifont-17.0.05.otf),
distributed under the SIL Open Font License 1.1 in `OFL-1.1.txt`. The PDF
renderer uses it only for characters IBM Plex does not cover (for example CJK),
so every recorded character is still drawn and extractable.

SHA-256: `85701ab9b1e251ee16f4df00b13f22eac311d72b7dab427a7d975fe7f5064702`

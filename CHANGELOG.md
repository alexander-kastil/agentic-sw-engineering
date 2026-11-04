# Changelog

All notable changes to this project will be documented in this file. See [commit-and-tag-version](https://github.com/absolute-version/commit-and-tag-version) for commit guidelines.

## 2026-11-04

### Added

- Plugin marketplaces subtopic in the class: I sent the team lead a reply
- Update .claude, .gitignore, .mcp.json
- Polyglot food app in `src/food-app`: Angular, React and Vue shops in `shop-ui/`, .NET, Java, Python, TypeScript and Go catalog APIs in `catalog-api/`, the Go API new.
- TypeScript QR code MCP server in `src/qr-server-ts`.

### Changed

- Demos and labs that use the food app point at the Angular shop and the .NET API by default, with a note on the other stacks; lab 08's solution follows the new Angular shop, whose test suite passes again.
- hr-mcp-server and qr-server-cs run on the latest packages; qr-server-cs pads QR codes with SkiaSharp and drops ImageSharp.
- qr-server-py pins every package to an exact version.
- Git no longer tracks `tasks/` and `agent-instructions/`.

## 2026-10-30

- The Claude `dotnet-conventions` copy drops its `dotnet-maf` index in favour of the `microsoft-agents:maf-dotnet` skill; the GitHub Copilot copy in `.github` keeps it.

## [Unreleased]

### Added

- Marketplace for the plugins demo (`demos/02-agentic-harness/06-plugins`), so the class can add the demo plugins from a local marketplace.
- Lab 04 on the plugin marketplace, with a team-plugins solution

### Changed

- Git ignores the time ledger (`.time/`), personal Claude settings and the scheduler lock, and no longer tracks the ledger.
- The labs after the new Lab 04 are renumbered

## 17.3.0 (2024-01-24)


### Features

* @ngrx/data standalone ([85d2d86](https://github.com/arambazamba/ng-adv/commit/85d2d86e2d1f4c7bb61b639147cf8042b8719f5d))
* Control-flow ([f5cad46](https://github.com/arambazamba/ng-adv/commit/f5cad467dfaef9a026960a3d1c38d9db430e5453))
* crud ([767b276](https://github.com/arambazamba/ng-adv/commit/767b27623530cf80a135b3a855dec9600b71b5b9))
* data-testid added to testing ([1a5029c](https://github.com/arambazamba/ng-adv/commit/1a5029cab75c298f3aa577b29ad74b4050ef50e9))
* firebase auth to standalone ([fe7177e](https://github.com/arambazamba/ng-adv/commit/fe7177e9b501d66ed7f21f7600a86d8e94e8aee3))
* save form for later ([8798042](https://github.com/arambazamba/ng-adv/commit/8798042f5bfb5d7233de7154a215e69c0d45a8bf))
* security lab to standalone and signals ([06ef575](https://github.com/arambazamba/ng-adv/commit/06ef57536ce04044d38692a373b6bf6553fea518))
* signal store lab ([bb738f3](https://github.com/arambazamba/ng-adv/commit/bb738f33fdb181d9cb86fef0ee1c4652b0d07e0d))
* walkthrough for standalone migration ([921ca1c](https://github.com/arambazamba/ng-adv/commit/921ca1c1d25fda21e407c7a37631c3e3b4e41650))


### Bug Fixes

* food-dashboard compilation ([de1493c](https://github.com/arambazamba/ng-adv/commit/de1493ce3e20e4c5bc2a7b0d4dcc33fff19097df))
* form updates ([209d1bd](https://github.com/arambazamba/ng-adv/commit/209d1bde8c61129cbc7e353034f0d981e3103512))
* labs partly migrated to 17 ([c0fbe0d](https://github.com/arambazamba/ng-adv/commit/c0fbe0d99978e18f4db06f6da8915c324d19f5b1))
* migrated to 17 ([465ad06](https://github.com/arambazamba/ng-adv/commit/465ad0665ce88bcafebffd5844d08bef6f3004c2))
* migration bugs in rxjs module fixed ([98d7356](https://github.com/arambazamba/ng-adv/commit/98d7356fae1432a9ab44aa65783feec233aa3eb6))
* rxjs typos ([05b0656](https://github.com/arambazamba/ng-adv/commit/05b0656fcd398e094bc47d7391c4880d76fa68be))
* typos in labguides fixed ([a8b85ad](https://github.com/arambazamba/ng-adv/commit/a8b85ad00ba8901de8d1ece50cc5b02a2e03d177))

## 17.2.0 (2024-01-21)


### Features

* @ngrx/data standalone ([85d2d86](https://github.com/arambazamba/ng-adv/commit/85d2d86e2d1f4c7bb61b639147cf8042b8719f5d))
* Control-flow ([f5cad46](https://github.com/arambazamba/ng-adv/commit/f5cad467dfaef9a026960a3d1c38d9db430e5453))
* crud ([767b276](https://github.com/arambazamba/ng-adv/commit/767b27623530cf80a135b3a855dec9600b71b5b9))
* signal store lab ([bb738f3](https://github.com/arambazamba/ng-adv/commit/bb738f33fdb181d9cb86fef0ee1c4652b0d07e0d))
* walkthrough for standalone migration ([921ca1c](https://github.com/arambazamba/ng-adv/commit/921ca1c1d25fda21e407c7a37631c3e3b4e41650))


### Bug Fixes

* labs partly migrated to 17 ([c0fbe0d](https://github.com/arambazamba/ng-adv/commit/c0fbe0d99978e18f4db06f6da8915c324d19f5b1))
* migrated to 17 ([465ad06](https://github.com/arambazamba/ng-adv/commit/465ad0665ce88bcafebffd5844d08bef6f3004c2))
* typos in labguides fixed ([a8b85ad](https://github.com/arambazamba/ng-adv/commit/a8b85ad00ba8901de8d1ece50cc5b02a2e03d177))

## 17.0.0 (2024-01-19)


### Features

* Control-flow ([f5cad46](https://github.com/arambazamba/ng-adv/commit/f5cad467dfaef9a026960a3d1c38d9db430e5453))
* crud ([767b276](https://github.com/arambazamba/ng-adv/commit/767b27623530cf80a135b3a855dec9600b71b5b9))
* signal store lab ([bb738f3](https://github.com/arambazamba/ng-adv/commit/bb738f33fdb181d9cb86fef0ee1c4652b0d07e0d))


### Bug Fixes

* labs partly migrated to 17 ([c0fbe0d](https://github.com/arambazamba/ng-adv/commit/c0fbe0d99978e18f4db06f6da8915c324d19f5b1))
* migrated to 17 ([465ad06](https://github.com/arambazamba/ng-adv/commit/465ad0665ce88bcafebffd5844d08bef6f3004c2))
* typos in labguides fixed ([a8b85ad](https://github.com/arambazamba/ng-adv/commit/a8b85ad00ba8901de8d1ece50cc5b02a2e03d177))

Name:           readest
Version:        0.9.93
Release:        0
Summary:        Modern, feature-rich ebook reader built with Tauri and Next.js
ExclusiveArch:  x86_64
License:        AGPL-3.0-or-later
URL:            https://github.com/readest/readest
Source0:        %{name}-%{version}.tar.gz
Source1:        vendor.tar.zst
Source2:        pnpm-store.tar.zst
Source3:        readest.desktop

BuildRequires:  cargo >= 1.77.2
BuildRequires:  rust >= 1.77.2
BuildRequires:  nodejs-common
BuildRequires:  npm
BuildRequires:  pnpm
BuildRequires:  pkgconfig(webkit2gtk-4.1)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(librsvg-2.0)
BuildRequires:  pkgconfig(ayatana-appindicator3-0.1)
BuildRequires:  pkgconfig(libsoup-3.0)
BuildRequires:  gcc-c++
BuildRequires:  desktop-file-utils

Requires:       libwebkit2gtk-4_1-0

%description
%{summary}.

%prep
%autosetup -n %{name}-%{version}
tar -I zstd -xf %{SOURCE1}
tar -I zstd -xf %{SOURCE2}

pnpm config set store-dir %{_builddir}/readest-%{version}/.pnpm-store

pnpm install --offline --frozen-lockfile

pnpm --filter @readest/readest-app setup-pdfjs

sed -i 's/"createUpdaterArtifacts": true/"createUpdaterArtifacts": false/' \
    apps/readest-app/src-tauri/tauri.conf.json

%build
pnpm tauri build --bundles rpm

%install
install -Dm755 target/release/readest \
    %{buildroot}%{_bindir}/readest

desktop-file-install --dir=%{buildroot}%{_datadir}/applications %{SOURCE3}

for size in 32 64 128 256; do
    if [ -f apps/readest-app/src-tauri/icons/${size}x${size}.png ]; then
        install -Dm644 apps/readest-app/src-tauri/icons/${size}x${size}.png \
            %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps/%{name}.png
    fi
done

%files
%license LICENSE
%doc README.md CONTRIBUTING.md
%{_bindir}/readest
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png

%changelog
* Sat Oct 26 2024 - 0.9.88-0
- Initial package

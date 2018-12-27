%undefine _strict_symbol_defs_build
%global pname QMPlay2

Name:           qmplay2
Version:        18.12.26
Release:        1%{?dist}
Summary:        A Qt based media player, streamer and downloader
License:        LGPLv3+
URL:            http://zaps166.sourceforge.net/?app=QMPlay2
Source:         https://github.com/zaps166/QMPlay2/archive/%{version}.tar.gz#/%{pname}-%{version}.tar.gz

BuildRequires:  cmake3
BuildRequires:  ninja-build
BuildRequires:  kde-workspace-devel
BuildRequires:  pkgconfig(Qt5) 
BuildRequires:  pkgconfig(Qt5X11Extras)
BuildRequires:  qt5-linguist
BuildRequires:  portaudio-devel
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(libass)
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  pkgconfig(libavdevice)
BuildRequires:  pkgconfig(libavformat)
BuildRequires:  pkgconfig(libavutil)
BuildRequires:  pkgconfig(libcddb)
BuildRequires:  pkgconfig(libcdio)
BuildRequires:  pkgconfig(libgme)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(libsidplayfp)
BuildRequires:  pkgconfig(libswresample)
BuildRequires:  pkgconfig(libswscale)
BuildRequires:  pkgconfig(libva)
BuildRequires:  pkgconfig(taglib)
BuildRequires:  pkgconfig(vdpau)
BuildRequires:  pkgconfig(xv)
Requires:       youtube-dl
Requires:       hicolor-icon-theme

%description
%{name} is a video player, it can play and stream all formats supported by
ffmpeg and libmodplug (including J2B). It has an integrated Youtube browser.

%package        kde-integration
Summary:        %{pname} KDE integration subpackage
Requires:       %{name} = %{version}-%{release}
Requires:       kde-workspace-common
BuildArch:      noarch

%description    kde-integration
Media playing actions for removable devices in KDE.

%package        devel
Summary:        %{pname} development files
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
It's a development package for %{name}.

%prep
%autosetup -p1 -n %{pname}-%{version}

# E: invalid-desktopfile /usr/share/applications/QMPlay2.desktop file
# contains group "PlayPause Shortcut Group", but groups extending the
# format should start with "X-"
sed -i '12,33d' src/gui/Unix/QMPlay2.desktop

%build
# Create translation files.
lrelease-qt5 QMPlay2.pro
mkdir -p %{_target_platform}
pushd %{_target_platform}
    %cmake \
    -DCMAKE_BUILD_TYPE='Debug' \
    -GNinja \
    ..
popd
%ninja_build -C %{_target_platform}

%install
%ninja_install -C %{_target_platform}

%find_lang %{name} --all-name --with-qt

# Let's use %%doc macro. AUTHORS & ChangeLog are required for help window
cd %{buildroot}/%{_datadir}/qmplay2
rm LICENSE README.md TODO AUTHORS ChangeLog

mkdir -p %{buildroot}%{_datadir}/appdata
mv %{buildroot}/%{_datadir}/metainfo/QMPlay2.appdata.xml \
   %{buildroot}/%{_metainfodir}/%{name}.appdata.xml

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.appdata.xml

%ldconfig_scriptlets

%files -f %{name}.lang
%doc AUTHORS ChangeLog README.md TODO
%license LICENSE
%{_bindir}/%{pname}
%{_libdir}/%{name}
%{_libdir}/libqmplay2.so
%{_datadir}/mime/packages/x-*.xml
%dir %{_datadir}/solid
%dir %{_datadir}/solid/actions
%{_datadir}/applications/%{pname}*.desktop
%{_metainfodir}/%{name}.appdata.xml
%{_datadir}/icons/hicolor/*/apps/%{pname}.*
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/lang
%{_mandir}/man1/%{pname}.1*

%files kde-integration
%{_datadir}/solid/actions/*.desktop

%files devel
%{_includedir}/%{pname}

%changelog
* Thu Dec 27 2018 Martin Gansser <martinkg@fedoraproject.org> - 18.12.26-1
- Update to 18.12.26

* Fri Nov 30 2018 Martin Gansser <martinkg@fedoraproject.org> - 18.11.20-1
- Update to 18.11.20

* Sun Aug 19 2018 Leigh Scott <leigh123linux@googlemail.com> - 18.07.03-2
- Rebuilt for Fedora 29 Mass Rebuild binutils issue

* Mon Jul 30 2018 Martin Gansser <martinkg@fedoraproject.org> - 18.07.03-1
- Update to 18.07.03

* Fri Jul 27 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 18.04.01-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jun 17 2018 Martin Gansser <martinkg@fedoraproject.org> - 18.04.01-1
- Update to 18.04.01

* Sun Jun 17 2018 Leigh Scott <leigh123linux@googlemail.com> - 18.03.02-2
- Rebuild for new libass version

* Fri Mar 09 2018 Martin Gansser <martinkg@fedoraproject.org> - 18.03.02-1
- Update to 18.03.02

* Thu Mar 08 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 17.12.31-7
- Rebuilt for new ffmpeg snapshot

* Thu Mar 01 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 17.12.31-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Feb 20 2018 Leigh Scott <leigh123linux@googlemail.com> - 17.12.31-5
- Rebuild for new ffmpeg snapshot
- Add build reqiures cmake3 and ninja-build
- Fix scriplets

* Sat Jan 27 2018 Leigh Scott <leigh123linux@googlemail.com> - 17.12.31-4
- Rebuild for new libcdio

* Thu Jan 18 2018 Leigh Scott <leigh123linux@googlemail.com> - 17.12.31-3
- Rebuilt for ffmpeg-3.5 git

* Mon Jan 15 2018 Nicolas Chauvet <kwizart@gmail.com> - 17.12.31-2
- Rebuilt for VA-API 1.0.0

* Sun Dec 31 2017 Martin Gansser <martinkg@fedoraproject.org> - 17.12.31-1
- Update to 17.12.31
- Added BR pkgconfig(Qt5X11Extras)

* Tue Dec 12 2017 Martin Gansser <martinkg@fedoraproject.org> - 17.12.11-1
- Update to 17.12.11

* Wed Oct 25 2017 Martin Gansser <martinkg@fedoraproject.org> - 17.10.24-1
- Update to 17.10.24

* Tue Oct 17 2017 Leigh Scott <leigh123linux@googlemail.com> - 17.10.04-2
- Rebuild for ffmpeg update

* Thu Oct 05 2017 Martin Gansser <martinkg@fedoraproject.org> - 17.10.04-1
- Update to 17.10.04

* Thu Sep 14 2017 Martin Gansser <martinkg@fedoraproject.org> - 17.09.13-1
- Update to 17.09.13

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 17.07.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul 26 2017 Martin Gansser <martinkg@fedoraproject.org> - 17.07.25-1
- Update to 17.07.25

* Sat Jun 10 2017 Martin Gansser <martinkg@fedoraproject.org> - 17.06.09-1
- Update to 17.06.09

* Mon Apr 03 2017 Martin Gansser <martinkg@fedoraproject.org> - 17.04.02-1
- Update to 17.04.02
- Dropped appdata.xml file

* Sat Mar 18 2017 Martin Gansser <martinkg@fedoraproject.org> - 17.03.17-1
- Update to 17.03.17
- Add appdata.xml file
- Add BR libappstream-glib

* Mon Feb 13 2017 Martin Gansser <martinkg@fedoraproject.org> - 17.02.12-1
- Update to 17.02.12

* Tue Dec 27 2016 Martin Gansser <martinkg@fedoraproject.org> - 16.12.23-1
- Update to 16.12.23

* Mon Nov 21 2016 Martin Gansser <martinkg@fedoraproject.org> - 16.11.20-1
- Update to 16.11.20

* Wed Nov 02 2016 Martin Gansser <martinkg@fedoraproject.org> - 16.11.01-1
- Update to 16.11.01

* Sun Oct 16 2016 Martin Gansser <martinkg@fedoraproject.org> - 16.10.14-1
- Update to 16.10.14

* Sun Sep 25 2016 Martin Gansser <martinkg@fedoraproject.org> - 16.09.24-1
- Update to 16.09.24

* Thu Sep 22 2016 Martin Gansser <martinkg@fedoraproject.org> - 16.09.21-1
- Update to 16.09.21

* Mon Sep 19 2016 Martin Gansser <martinkg@fedoraproject.org> - 16.09.17-1
- Update to 16.09.17

* Mon Sep 05 2016 Martin Gansser <martinkg@fedoraproject.org> - 16.09.04-1
- Update to 16.09.04

* Sat Sep 03 2016 Martin Gansser <martinkg@fedoraproject.org> - 16.08.19-4
- removed %%_isa requirement from kde-integration subpackage

* Tue Aug 23 2016 Martin Gansser <martinkg@fedoraproject.org> - 16.08.19-3
- Take ownership of directory %%{_datadir}/solid and %%{_datadir}/solid/actions
- Removed call to gzip manpage file and added 
  %%{_mandir}/man1/%%{pname}.1 to %%files section
- Removed installation folder for doc files 
- Changed if condition for installing system libdir
- Used macro %%autosetup
- Dropped %%{pname}-debug-info.patch
- Used %%{_datadir}/%%{name} for lang files
- Switched build commmand to %%cmake
- spec file cleanup

* Mon Aug 22 2016 Martin Gansser <martinkg@fedoraproject.org> - 16.08.19-2
- Changed qt5-qtbase-devel to pkgconfig(Qt5)
- Removed QT4 BR pkgconfig(QtCore)

* Sat Aug 20 2016 Martin Gansser <martinkg@fedoraproject.org> - 16.08.19-1
- Update to 16.08.19

* Wed Jul 27 2016 Martin Gansser <martinkg@fedoraproject.org> - 16.07.20-1
- Update to 16.07.20

* Thu Jun 09 2016 Martin Gansser <martinkg@fedoraproject.org> - 16.06.01-2
- Added %%check section for desktop file

* Thu Jun 02 2016 Martin Gansser <martinkg@fedoraproject.org> - 16.06.01-1
- Update to 16.06.01

* Tue May 03 2016 Martin Gansser <martinkg@fedoraproject.org> - 16.05.02-1
- Update to 16.05.02

* Sun Apr 24 2016 Martin Gansser <martinkg@fedoraproject.org> - 16.04.23-1
- Update to 16.04.23

* Fri Mar 25 2016 Martin Gansser <martinkg@fedoraproject.org> - 16.03.24-1
- Update to 16.03.24

* Sat Mar 12 2016 Martin Gansser <martinkg@fedoraproject.org> - 16.03.11-1
- Update to 16.03.11

* Fri Mar 11 2016 Martin Gansser <martinkg@fedoraproject.org> - 16.03.08-2
- Added patch %%{pname}-debug-info.patch

* Wed Mar 09 2016 Martin Gansser <martinkg@fedoraproject.org> - 16.03.08-1
- Initial build

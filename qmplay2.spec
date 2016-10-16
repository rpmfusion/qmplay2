%global pname QMPlay2

Name:           qmplay2
Version:        16.10.14
Release:        1%{?dist}
Summary:        A Qt based media player, streamer and downloader
License:        LGPLv3+
Url:            http://zaps166.sourceforge.net/?app=QMPlay2
Source:         https://github.com/zaps166/QMPlay2/releases/download/%{version}/%{pname}-src-%{version}.tar.xz

BuildRequires:  kde-workspace-devel
BuildRequires:  pkgconfig(Qt5) 
BuildRequires:  qt5-linguist
BuildRequires:  portaudio-devel
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
%autosetup -n %{pname}-src-%{version}

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
    ..
popd
%make_build -C %{_target_platform}

%install
%make_install -C %{_target_platform}

find %{buildroot}%{_datadir}/%{name} -name "*.qm" | sed 's:'%{buildroot}'::
s:.*/\([a-zA-Z]\{2\}\).qm:%lang(\1) \0:' > %{name}.lang

# Let's use %%doc macro. AUTHORS & ChangeLog are required for help window
cd %{buildroot}/%{_datadir}/qmplay2
rm LICENSE README.md TODO AUTHORS ChangeLog

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop

%post
/sbin/ldconfig
/usr/bin/update-mime-database %{_datadir}/mime &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
/usr/bin/update-desktop-database &> /dev/null || :

%postun
/sbin/ldconfig
if [ $1 -eq 0 ] ; then
  /usr/bin/update-mime-database %{_datadir}/mime &> /dev/null || :
  touch --no-create %{_datadir}/icons/hicolor &>/dev/null
  /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
/usr/bin/update-desktop-database &> /dev/null || :

%posttrans
/usr/bin/update-mime-database %{?fedora:-n} %{_datadir}/mime &> /dev/null || :
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

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
%{_datadir}/icons/hicolor/*/apps/%{pname}.png
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/lang
%{_mandir}/man1/%{pname}.1*

%files kde-integration
%{_datadir}/solid/actions/*.desktop

%files devel
%{_includedir}/%{pname}

%changelog
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

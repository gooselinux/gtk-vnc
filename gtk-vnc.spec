# -*- rpm-spec -*-

# Plugin isn't ready for real world use yet - it needs
# a security audit at very least
%define with_plugin 0

Summary: A GTK widget for VNC clients
Name: gtk-vnc
Version: 0.3.10
Release: 3%{?dist}
License: LGPLv2+
Group: Development/Libraries
Source: http://ftp.gnome.org/pub/GNOME/sources/%{name}/0.3/%{name}-%{version}.tar.bz2
Patch1: %{name}-%{version}-gcrypt-threading.patch
Patch2: %{name}-%{version}-bounds.patch
Patch3: %{name}-%{version}-ipv6-conn.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
URL: http://live.gnome.org/gtk-vnc
BuildRequires: gtk2-devel pygtk2-devel python-devel zlib-devel
BuildRequires: gnutls-devel cyrus-sasl-devel
BuildRequires: intltool
%if %{with_plugin}
%if 0%{?fedora} > 8 || 0%{?rhel} >= 6
BuildRequires: xulrunner-devel
%else
BuildRequires: firefox-devel
%endif
%endif

%description
gtk-vnc is a VNC viewer widget for GTK. It is built using coroutines
allowing it to be completely asynchronous while remaining single threaded.

%package devel
Summary: Libraries, includes, etc. to compile with the gtk-vnc library
Group: Development/Libraries
Requires: %{name} = %{version}
Requires: pkgconfig
Requires: gtk2-devel gnutls-devel

%description devel
gtk-vnc is a VNC viewer widget for GTK. It is built using coroutines
allowing it to be completely asynchronous while remaining single threaded.

Libraries, includes, etc. to compile with the gtk-vnc library

%package python
Summary: Python bindings for the gtk-vnc library
Group: Development/Libraries
Requires: %{name} = %{version}

%description python
gtk-vnc is a VNC viewer widget for GTK. It is built using coroutines
allowing it to be completely asynchronous while remaining single threaded.

A module allowing use of the GTK-VNC widget from python

%if %{with_plugin}
%package plugin
Summary: Mozilla plugin for the gtk-vnc library
Group: Development/Libraries
Requires: %{name} = %{version}

%description plugin
gtk-vnc is a VNC viewer widget for GTK. It is built using coroutines
allowing it to be completely asynchronous while remaining single threaded.

This package provides a web browser plugin for Mozilla compatible
browsers.
%endif

%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%if %{with_plugin}
%configure --enable-plugin=yes
%else
%configure
%endif
%__make %{?_smp_mflags}

%install
rm -fr %{buildroot}
%__make install DESTDIR=%{buildroot}
rm -f %{buildroot}%{_libdir}/*.a
rm -f %{buildroot}%{_libdir}/*.la
rm -f %{buildroot}%{_libdir}/python*/site-packages/*.a
rm -f %{buildroot}%{_libdir}/python*/site-packages/*.la
%if %{with_plugin}
rm -f %{buildroot}%{_libdir}/mozilla/plugins/%{name}-plugin.a
rm -f %{buildroot}%{_libdir}/mozilla/plugins/%{name}-plugin.la
%endif

%find_lang gtk-vnc

%clean
rm -fr %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f gtk-vnc.lang
%defattr(-, root, root)
%doc AUTHORS ChangeLog NEWS README COPYING.LIB
%{_libdir}/lib*.so.*

%files devel
%defattr(-, root, root)
%doc examples/gvncviewer.c
%{_libdir}/lib*.so
%dir %{_includedir}/%{name}-1.0/
%{_includedir}/%{name}-1.0/*.h
%{_libdir}/pkgconfig/%{name}-1.0.pc

%files python
%defattr(-, root, root)
%doc examples/gvncviewer.py
%{_libdir}/python*/site-packages/gtkvnc.so

%if %{with_plugin}
%files plugin
%defattr(-, root, root)
%{_libdir}/mozilla/plugins/%{name}-plugin.so
%endif

%changelog
* Tue Jun  8 2010 Daniel P. Berrange <berrange@redhat.com> - 0.3.10-3
- Try next DNS addr on all connect errors (rhbz #588320)

* Thu May 13 2010 Daniel P. Berrange <berrange@redhat.com> - 0.3.10-2
- Drop VNC connection if the server sends a update spaning outside bounds of desktop (rhbz #590068)
- Fix gcrypt threading initialization (rhbz #591827)

* Fri Nov 13 2009 Dennis Gregorovic <dgregor@redhat.com> - 0.3.10-1.1
- Fix conditional for RHEL

* Tue Oct 20 2009 Matthias Clasen <mclaesn@redhat.com> - 0.3.10-1
- Update to 0.3.10

* Thu Oct  8 2009 Matthias Clasen <mclaesn@redhat.com> - 0.3.9-2
- Request a full screen refresh when receives a desktop-resize encoding

* Tue Aug 11 2009 Daniel P. Berrange <berrange@redhat.com> - 0.3.9-1
- Update to 0.3.9 release

* Tue Aug 11 2009 Ville Skyttä <ville.skytta@iki.fi> - 0.3.8-10
- Use bzipped upstream tarball.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.8-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Mar 27 2009 Daniel P. Berrange <berrange@redhat.com> - 0.3.8-8.fc11
- Fix ungrab when pointer type changes

* Tue Mar 24 2009 Daniel P. Berrange <berrange@redhat.com> - 0.3.8-7.fc11
- Fix release of keyboard grab when releasing mouse grab outside app window (rhbz #491167)

* Thu Mar  5 2009 Daniel P. Berrange <berrange@redhat.com> - 0.3.8-6.fc11
- Fix SASL address generation when using AF_UNIX sockets

* Tue Mar  3 2009 Daniel P. Berrange <berrange@redhat.com> - 0.3.8-5.fc11
- Support SASL authentication extension

* Thu Feb 26 2009 Daniel P. Berrange <berrange@redhat.com> - 0.3.8-4.fc11
- Fix relative mouse handling to avoid 'invisible wall'

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.8-3.fc11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 24 2009 Daniel P. Berrange <berrange@redhat.com> - 0.3.8-2.fc11
- Update URLs to gnome.org hosting

* Sun Dec  7 2008 Daniel P. Berrange <berrange@redhat.com> - 0.3.8-1.fc11
- Update to 0.3.8 release

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.3.7-4
- Rebuild for Python 2.6

* Thu Oct  9 2008 Daniel P. Berrange <berrange@redhat.com> - 0.3.7-3.fc10
- Avoid bogus framebuffer updates for psuedo-encodings
- Fix scancode translation for evdev

* Thu Sep 25 2008 Daniel P. Berrange <berrange@redhat.com> - 0.3.7-2.fc10
- Allow pointer ungrab keysequence if already grabbed (rhbz #463729)

* Fri Sep  5 2008 Matthias Clasen  <mclasen@redhat.com> - 0.3.7-1
- Update to 0.3.7

* Thu Aug 28 2008 Daniel P. Berrange <berrange@redhat.com> - 0.3.6-4.fc10
- Fix key/mouse event propagation (rhbz #454627)

* Mon Jul  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.3.6-3
- fix conditional comparison

* Wed Jun 25 2008 Daniel P. Berrange <berrange@redhat.com> - 0.3.6-2.fc10
- Rebuild for GNU TLS ABI change

* Wed May  7 2008 Daniel P. Berrange <berrange@redhat.com> - 0.3.6-1.fc10
- Updated to 0.3.6 release

* Fri Apr 25 2008 Matthias Clasen <mclasen@redhat.com> - 0.3.5-1.fc9
- Update to 0.3.5

* Fri Apr  4 2008 Daniel P. Berrange <berrange@redhat.com> - 0.3.4-4.fc9
- Remove bogus chunk of render patch

* Thu Apr  3 2008 Daniel P. Berrange <berrange@redhat.com> - 0.3.4-3.fc9
- Fix OpenGL rendering artifacts (rhbz #440184)

* Thu Apr  3 2008 Daniel P. Berrange <berrange@redhat.com> - 0.3.4-2.fc9
- Fixed endianness conversions
- Fix makecontext() args crash on x86_64
- Fix protocol version negotiation

* Thu Mar  6 2008 Daniel P. Berrange <berrange@redhat.com> - 0.3.4-1.fc9
- Update to 0.3.4 release
- Fix crash with OpenGL scaling code

* Sun Feb  3 2008 Daniel P. Berrange <berrange@redhat.com> - 0.3.3-1.fc9
- Update to 0.3.3 release

* Mon Jan 14 2008 Daniel P. Berrange <berrange@redhat.com> - 0.3.2-2.fc9
- Track keystate to avoid stuck modifier keys

* Mon Dec 31 2007 Daniel P. Berrange <berrange@redhat.com> - 0.3.2-1.fc9
- Update to 0.3.2 release
- Added dep on zlib-devel

* Thu Dec 13 2007 Daniel P. Berrange <berrange@redhat.com> - 0.3.1-1.fc9
- Update to 0.3.1 release

* Thu Oct 10 2007 Daniel P. Berrange <berrange@redhat.com> - 0.2.0-4.fc8
- Fixed coroutine cleanup to avoid SEGV (rhbz #325731)

* Thu Oct  4 2007 Daniel P. Berrange <berrange@redhat.com> - 0.2.0-3.fc8
- Fixed coroutine caller to avoid SEGV

* Wed Sep 26 2007 Daniel P. Berrange <berrange@redhat.com> - 0.2.0-2.fc8
- Remove use of PROT_EXEC for coroutine stack (rhbz #307531 )

* Thu Sep 13 2007 Daniel P. Berrange <berrange@redhat.com> - 0.2.0-1.fc8
- Update to 0.2.0 release

* Wed Aug 29 2007 Daniel P. Berrange <berrange@redhat.com> - 0.1.0-5.fc8
- Fixed handling of mis-matched client/server colour depths

* Wed Aug 22 2007 Daniel P. Berrange <berrange@redhat.com> - 0.1.0-4.fc8
- Fix mixed endian handling & BGR pixel format (rhbz #253597)
- Clear widget areas outside of framebuffer (rhbz #253599)
- Fix off-by-one in python demo

* Thu Aug 16 2007 Daniel P. Berrange <berrange@redhat.com> - 0.1.0-3.fc8
- Tweaked post scripts
- Removed docs from sub-packages
- Explicitly set license to LGPLv2+
- Remove use of macro for install rule

* Wed Aug 15 2007 Daniel P. Berrange <berrange@redhat.com> - 0.1.0-2.fc8
- Added gnutls-devel requirement to -devel package

* Wed Aug 15 2007 Daniel P. Berrange <berrange@redhat.com> - 0.1.0-1.fc8
- Initial official release

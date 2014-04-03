Summary:	GstRTCP - an RTSP server built on top of GStreamer
Summary(pl.UTF-8):	GstRTSP - serwer RTSP zbudowany w oparciu o GStreamera
Name:		gstreamer-rtsp-server
Version:	1.2.3
Release:	2
License:	LGPL v2+
Group:		Libraries
Source0:	http://gstreamer.freedesktop.org/src/gst-rtsp-server/gst-rtsp-server-%{version}.tar.xz
# Source0-md5:	239f805e755deb388162e957fcffff1d
URL:		http://gstreamer.net/
BuildRequires:	autoconf >= 2.62
BuildRequires:	automake >= 1:1.11
BuildRequires:	glib2-devel >= 1:2.32.0
BuildRequires:	gobject-introspection-devel >= 1.31.1
BuildRequires:	gstreamer-devel >= 1.2.3
BuildRequires:	gstreamer-plugins-base-devel >= 1.2.3
BuildRequires:	gtk-doc >= 1.12
BuildRequires:	libcgroup-devel >= 0.26
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	glib2 >= 1:2.32.0
Requires:	gstreamer >= 1.2.3
Requires:	gstreamer-plugins-base >= 1.2.3
Requires:	libcgroup >= 0.26
Obsoletes:	gstreamer-rtsp < 1.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GstRTSP is an RTSP server built on top of GStreamer.

%description -l pl.UTF-8
GstRTSP to serwer RTSP zbudowany w oparciu o GStreamera.

%package devel
Summary:	Header files for GstRTSPserver library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki GstRTSPserver
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.32.0
Requires:	gstreamer-devel >= 1.2.3
Requires:	gstreamer-plugins-base-devel >= 1.2.3
Obsoletes:	gstreamer-rtsp-devel < 1.1

%description devel
Header files for GstRTSPserver library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki GstRTSPserver.

%package apidocs
Summary:	API documentation for GstRTSPserver library
Summary(pl.UTF-8):	Dokumentacja API biblioteki GstRTSPserver
Group:		Documentation
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
API documentation for GstRTSPserver library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki GstRTSPserver.

%prep
%setup -q -n gst-rtsp-server-%{version}

%build
%{__libtoolize}
%{__aclocal} -I m4 -I common/m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-gtk-doc \
	--disable-silent-rules \
	--disable-static \
	--with-html-dir=%{_gtkdocdir}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README TODO docs/design/gst-rtp-server-design
%attr(755,root,root) %{_libdir}/libgstrtspserver-1.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgstrtspserver-1.0.so.0
%{_libdir}/girepository-1.0/GstRtspServer-1.0.typelib

%files devel
%defattr(644,root,root,755)
%doc docs/README
%attr(755,root,root) %{_libdir}/libgstrtspserver-1.0.so
%{_includedir}/gstreamer-1.0/gst/rtsp-server
%{_pkgconfigdir}/gstreamer-rtsp-server-1.0.pc
%{_datadir}/gir-1.0/GstRtspServer-1.0.gir

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/gst-rtsp-server-1.0

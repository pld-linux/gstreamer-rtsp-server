%define		gst_ver		1.8.0
%define		gstpb_ver	1.8.0
%define		gstpg_ver	1.8.0
%define		gstpd_ver	1.8.0
Summary:	GstRTCP - an RTSP server built on top of GStreamer
Summary(pl.UTF-8):	GstRTSP - serwer RTSP zbudowany w oparciu o GStreamera
Name:		gstreamer-rtsp-server
Version:	1.8.1
Release:	1
License:	LGPL v2+
Group:		Libraries
Source0:	https://gstreamer.freedesktop.org/src/gst-rtsp-server/gst-rtsp-server-%{version}.tar.xz
# Source0-md5:	0a5966df7f3d74cccfcededdcacd8212
URL:		https://gstreamer.freedesktop.org/
BuildRequires:	autoconf >= 2.69
BuildRequires:	automake >= 1:1.14
BuildRequires:	glib2-devel >= 1:2.40.0
BuildRequires:	gobject-introspection-devel >= 1.31.1
BuildRequires:	gstreamer-devel >= %{gst_ver}
# only for message
#BuildRequires:	gstreamer-plugins-bad-devel >= %{gstpd_ver}
BuildRequires:	gstreamer-plugins-base-devel >= %{gstpb_ver}
# only for message
#BuildRequires:	gstreamer-plugins-good-devel >= %{gstpg_ver}
BuildRequires:	gtk-doc >= 1.12
BuildRequires:	libcgroup-devel >= 0.26
BuildRequires:	libtool >= 2:2.2.6
BuildRequires:	pkgconfig >= 1:0.9.0
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	glib2 >= 1:2.40.0
Requires:	gstreamer >= %{gst_ver}
Requires:	gstreamer-plugins-base >= %{gstpb_ver}
Requires:	libcgroup-libs >= 0.26
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
Requires:	glib2-devel >= 1:2.40.0
Requires:	gstreamer-devel >= %{gst_ver}
Requires:	gstreamer-plugins-base-devel >= %{gstpb_ver}
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
# glib-loadable module
%{__rm} $RPM_BUILD_ROOT%{_libdir}/gstreamer-1.0/libgstrtspclientsink.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README RELEASE TODO docs/design/gst-rtp-server-design
%attr(755,root,root) %{_libdir}/libgstrtspserver-1.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgstrtspserver-1.0.so.0
%{_libdir}/girepository-1.0/GstRtspServer-1.0.typelib
%attr(755,root,root) %{_libdir}/gstreamer-1.0/libgstrtspclientsink.so

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

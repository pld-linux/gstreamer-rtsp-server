#
# Conditional build:
%bcond_without	apidocs	# API documentation

%define		gst_ver		1.22.0
%define		gstpb_ver	1.22.0
%define		gstpg_ver	1.22.0
%define		gstpd_ver	1.22.0
Summary:	GstRTCP - an RTSP server built on top of GStreamer
Summary(pl.UTF-8):	GstRTSP - serwer RTSP zbudowany w oparciu o GStreamera
Name:		gstreamer-rtsp-server
Version:	1.22.6
Release:	1
License:	LGPL v2+
Group:		Libraries
Source0:	https://gstreamer.freedesktop.org/src/gst-rtsp-server/gst-rtsp-server-%{version}.tar.xz
# Source0-md5:	d887bf97d4208233cb833afe9a8bf0ac
URL:		https://gstreamer.freedesktop.org/
BuildRequires:	glib2-devel >= 1:2.62.0
BuildRequires:	gobject-introspection-devel >= 1.31.1
BuildRequires:	gstreamer-devel >= %{gst_ver}
# only for message
#BuildRequires:	gstreamer-plugins-bad-devel >= %{gstpd_ver}
BuildRequires:	gstreamer-plugins-base-devel >= %{gstpb_ver}
# only for message
#BuildRequires:	gstreamer-plugins-good-devel >= %{gstpg_ver}
%{?with_apidocs:BuildRequires:	hotdoc >= 0.11.0}
# for test-cgroups example
#BuildRequires:	libcgroup-devel >= 0.26
BuildRequires:	meson >= 0.62
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig >= 1:0.9.0
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	glib2 >= 1:2.62.0
Requires:	gstreamer >= %{gst_ver}
Requires:	gstreamer-plugins-base >= %{gstpb_ver}
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
Requires:	glib2-devel >= 1:2.62.0
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
BuildArch:	noarch

%description apidocs
API documentation for GstRTSPserver library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki GstRTSPserver.

%prep
%setup -q -n gst-rtsp-server-%{version}

%build
%meson build \
	--default-library=shared \
	%{!?with_apidocs:-Ddoc=false}

%ninja_build -C build

%if %{with apidocs}
cd build/docs
for component in gst-rtsp-server rtspclientsink ; do
	LC_ALL=C.UTF-8 hotdoc run --conf-file ${component}-doc.json
done
%endif

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%if %{with apidocs}
install -d $RPM_BUILD_ROOT%{_docdir}/gstreamer-%{gstmver}
cp -pr build/docs/{gst-rtsp-server,rtspclientsink}-doc $RPM_BUILD_ROOT%{_docdir}/gstreamer-%{gstmver}
%endif

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

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_docdir}/gstreamer-%{gstmver}/gst-rtsp-server-doc
%{_docdir}/gstreamer-%{gstmver}/rtspclientsink-doc
%endif

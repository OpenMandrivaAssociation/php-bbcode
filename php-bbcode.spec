%define modname bbcode
%define dirname %{modname}
%define soname %{modname}.so
%define inifile A68_%{modname}.ini

Summary:	BBCode parsing Extension
Name:		php-%{modname}
Version:	1.0.3
Release:	%mkrel 0.0.b1.6
Group:		Development/PHP
License:	PHP License
URL:		https://pecl.php.net/package/bbcode
Source0:	http://pecl.php.net/get/%{modname}-%{version}b1.tgz
BuildRequires:	php-devel >= 3:5.2.0
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
This is a quick and efficient BBCode Parsing Library. It provides various tag
types, high speed one pass parsing, callback system, tag position restriction.

It will force closing BBCode tags in the good order, and closing terminating
tags at the end of the string this is in order to ensure HTML Validity in all
case.

%prep

%setup -q -n %{modname}-%{version}b1
[ "../package*.xml" != "/" ] && mv ../package*.xml .

%build
%serverbuild

#export CFLAGS="%(echo %optflags | sed 's/-Wp,-D_FORTIFY_SOURCE=2//')"
#export CXXFLAGS="${CFLAGS}"
#export CCFLAGS="${CFLAGS}"

phpize
%configure2_5x --with-libdir=%{_lib} \
    --with-%{modname}=shared,%{_prefix}
%make

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m755 .libs/%{soname} %{buildroot}%{_libdir}/php/extensions/

cat > %{buildroot}%{_sysconfdir}/php.d/%{inifile} << EOF
extension = %{soname}
EOF

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart >/dev/null || :
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart >/dev/null || :
    fi
fi

%clean
rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc CREDITS package*.xml
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}


%changelog
* Thu May 03 2012 Oden Eriksson <oeriksson@mandriva.com> 1.0.3-0.0.b1.6mdv2012.0
+ Revision: 795401
- rebuild for php-5.4.x

* Sun Jan 15 2012 Oden Eriksson <oeriksson@mandriva.com> 1.0.3-0.0.b1.5
+ Revision: 761200
- rebuild

* Wed Aug 24 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.3-0.0.b1.4
+ Revision: 696393
- rebuilt for php-5.3.8

* Fri Aug 19 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.3-0.0.b1.3
+ Revision: 695362
- rebuilt for php-5.3.7

* Sat Mar 19 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.3-0.0.b1.2
+ Revision: 646612
- rebuilt for php-5.3.6

* Sat Jan 08 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.3-0.0.b1.1mdv2011.0
+ Revision: 630290
- 1.0.3b1

* Sat Jan 08 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-15mdv2011.0
+ Revision: 629765
- rebuilt for php-5.3.5

* Mon Jan 03 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-14mdv2011.0
+ Revision: 628067
- ensure it's built without automake1.7

* Wed Nov 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-13mdv2011.0
+ Revision: 600461
- rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-12mdv2011.0
+ Revision: 588743
- rebuild

* Fri Mar 05 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-11mdv2010.1
+ Revision: 514518
- rebuilt for php-5.3.2

* Sat Jan 02 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-10mdv2010.1
+ Revision: 485339
- rebuilt for php-5.3.2RC1

* Sat Nov 21 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-9mdv2010.1
+ Revision: 468144
- rebuilt against php-5.3.1

* Wed Sep 30 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-8mdv2010.0
+ Revision: 451253
- rebuild

* Sun Jul 19 2009 Raphaël Gertz <rapsys@mandriva.org> 1.0.2-7mdv2010.0
+ Revision: 397265
- Rebuild

* Mon May 18 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-6mdv2010.0
+ Revision: 376973
- rebuilt for php-5.3.0RC2

* Sun Mar 01 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-5mdv2009.1
+ Revision: 346395
- rebuilt for php-5.2.9

* Tue Feb 17 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-4mdv2009.1
+ Revision: 341708
- rebuilt against php-5.2.9RC2

* Wed Dec 31 2008 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-3mdv2009.1
+ Revision: 321703
- rebuild

* Fri Dec 05 2008 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-2mdv2009.1
+ Revision: 310249
- rebuilt against php-5.2.7

* Tue Aug 19 2008 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-1mdv2009.0
+ Revision: 273798
- 1.0.2

* Sun Aug 17 2008 Oden Eriksson <oeriksson@mandriva.com> 1.0.1-1mdv2009.0
+ Revision: 272910
- 1.0.1

* Fri Jul 18 2008 Oden Eriksson <oeriksson@mandriva.com> 0.10.4-5mdv2009.0
+ Revision: 238377
- rebuild

* Fri May 02 2008 Oden Eriksson <oeriksson@mandriva.com> 0.10.4-4mdv2009.0
+ Revision: 200187
- rebuilt for php-5.2.6

* Mon Feb 04 2008 Oden Eriksson <oeriksson@mandriva.com> 0.10.4-3mdv2008.1
+ Revision: 162155
- rebuild

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Nov 11 2007 Oden Eriksson <oeriksson@mandriva.com> 0.10.4-2mdv2008.1
+ Revision: 107606
- restart apache if needed

* Thu Oct 25 2007 Oden Eriksson <oeriksson@mandriva.com> 0.10.4-1mdv2008.1
+ Revision: 102091
- 0.10.4
- import php-bbcode


* Sat Oct 13 2007 Oden Eriksson <oeriksson@mandriva.com> 0.10.3-1mdv2008.1
- initial Mandriva package

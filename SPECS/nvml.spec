
# rpmbuild options:
#   --with | --without ndctl

# do not terminate build if files in the $RPM_BUILD_ROOT
# directory are not found in %%files (without pmemcheck case)
%define _unpackaged_files_terminate_build 0

# disable 'make check'
%define _skip_check 1

# by default build with ndctl, unless explicitly disabled
%bcond_without ndctl

# by default build without pmemcheck, unless explicitly enabled
# pmemcheck is not packaged by Fedora
%bcond_with pmemcheck

%define min_ndctl_ver 60.1
%define upstreamversion 1.12.1

Name:		nvml
Version:	1.12.1
Release:	1%{?dist}
Summary:	Persistent Memory Development Kit (formerly NVML)
License:	BSD
URL:		http://pmem.io/pmdk

Source0:	https://github.com/pmem/pmdk/releases/download/%{upstreamversion}/pmdk-%{upstreamversion}.tar.gz
# RHEL 9 does not ship pandoc, so the man pages have to be generated
# on another operating system (such as fedora or RHEL 8).  To do that,
# run the included makedocs.sh script on a system with pandoc.
Source1:	pmdk-%{version}-man.tar.gz

# do_open passes "attr" to util_pool_open which potentially reads that object
# but do_open never initializes "attr"
# may read that object
Patch0:         Makefile-bypass-check-doc-in-check.patch
Patch1:         pmdk-1.12.1-use_ddebug_instead_of_debug_cflags.patch


BuildRequires:	gcc
BuildRequires:	make
BuildRequires:	cmake
BuildRequires:	glibc-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	man
BuildRequires:	pkgconfig
BuildRequires:	python3
BuildRequires:	groff

%if %{with ndctl}
BuildRequires:	ndctl-devel >= %{min_ndctl_ver}
BuildRequires:	daxctl-devel >= %{min_ndctl_ver}
%endif

# for tests
BuildRequires:	gdb
BuildRequires:	bc
#BuildRequires:	valgrind

# Debug variants of the libraries should be filtered out of the provides.
%global __provides_exclude_from ^%{_libdir}/pmdk_debug/.*\\.so.*$

# By design, PMDK does not support any 32-bit architecture.
# Due to dependency on some inline assembly, PMDK can be compiled only
# on these architectures:
# - x86_64
# - ppc64le (experimental)
# - aarch64 (unmaintained, supporting hardware doesn't exist?)
#
# Other 64-bit architectures could also be supported, if only there is
# a request for that, and if somebody provides the arch-specific
# implementation of the low-level routines for flushing to persistent
# memory.

# https://bugzilla.redhat.com/show_bug.cgi?id=1340634
# https://bugzilla.redhat.com/show_bug.cgi?id=1340635
# https://bugzilla.redhat.com/show_bug.cgi?id=1340637

ExclusiveArch: x86_64 ppc64le

%description
The Persistent Memory Development Kit is a collection of libraries for
using memory-mapped persistence, optimized specifically for persistent memory.


%package -n libpmem
Summary: Low-level persistent memory support library
%description -n libpmem
The libpmem provides low level persistent memory support. In particular,
support for the persistent memory instructions for flushing changes
to pmem is provided.  This package provides the v1 API.

%files -n libpmem
%dir %{_datadir}/pmdk
%{_libdir}/libpmem.so.*
%{_datadir}/pmdk/pmdk.magic
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md


%package -n libpmem-devel
Summary: Development files for the low-level persistent memory library
Requires: libpmem = %{version}-%{release}
%description -n libpmem-devel
The libpmem provides low level persistent memory support. In particular,
support for the persistent memory instructions for flushing changes
to pmem is provided. This package provides the v1 API.

This library is provided for software which tracks every store to
pmem and needs to flush those changes to durability. Most developers
will find higher level libraries like libpmemobj to be much more
convenient.

%files -n libpmem-devel
%{_libdir}/libpmem.so
%{_libdir}/pkgconfig/libpmem.pc
%{_includedir}/libpmem.h
%{_mandir}/man7/libpmem.7.gz
%{_mandir}/man3/pmem_*.3.gz
%{_mandir}/man5/pmem_ctl.5.gz
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md


%package -n libpmem-debug
Summary: Debug variant of the low-level persistent memory library
Requires: libpmem = %{version}-%{release}
%description -n libpmem-debug
The libpmem provides low level persistent memory support. In particular,
support for the persistent memory instructions for flushing changes
to pmem is provided. This package provides the v1 API.

This sub-package contains debug variant of the library, providing
run-time assertions and trace points. The typical way to access the
debug version is to set the environment variable LD_LIBRARY_PATH to
/usr/lib64/pmdk_debug.

%files -n libpmem-debug
%dir %{_libdir}/pmdk_debug
%{_libdir}/pmdk_debug/libpmem.so
%{_libdir}/pmdk_debug/libpmem.so.*
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md


%package -n libpmem2
Summary: Low-level persistent memory support library
%description -n libpmem2
The libpmem provides low level persistent memory support. In particular,
support for the persistent memory instructions for flushing changes
to pmem is provided. This package provides the v2 API.

%files -n libpmem2
%dir %{_datadir}/pmdk
%{_libdir}/libpmem2.so.*
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md


%package -n libpmem2-devel
Summary: Development files for the low-level persistent memory library
Requires: libpmem = %{version}-%{release}
%description -n libpmem2-devel
The libpmem provides low level persistent memory support. In particular,
support for the persistent memory instructions for flushing changes
to pmem is provided. This package provides the v2 API.

This library is provided for software which tracks every store to
pmem and needs to flush those changes to durability. Most developers
will find higher level libraries like libpmemobj to be much more
convenient.

%files -n libpmem2-devel
%{_libdir}/libpmem2.so
%{_libdir}/pkgconfig/libpmem2.pc
%{_includedir}/libpmem2.h
%{_mandir}/man7/libpmem2*7.gz
%{_mandir}/man3/pmem2_*.3.gz
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md


%package -n libpmem2-debug
Summary: Debug variant of the low-level persistent memory library
Requires: libpmem = %{version}-%{release}
%description -n libpmem2-debug
The libpmem provides low level persistent memory support. In particular,
support for the persistent memory instructions for flushing changes
to pmem is provided. This package provides the v2 API.

This sub-package contains debug variant of the library, providing
run-time assertions and trace points. The typical way to access the
debug version is to set the environment variable LD_LIBRARY_PATH to
/usr/lib64/pmdk_debug.

%files -n libpmem2-debug
%dir %{_libdir}/pmdk_debug
%{_libdir}/pmdk_debug/libpmem2.so
%{_libdir}/pmdk_debug/libpmem2.so.*
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md


%package -n libpmemblk
Summary: Persistent Memory Resident Array of Blocks library
Requires: libpmem >= %{version}-%{release}
%description -n libpmemblk
The libpmemblk implements a pmem-resident array of blocks, all the same
size, where a block is updated atomically with respect to power
failure or program interruption (no torn blocks).

%files -n libpmemblk
%{_libdir}/libpmemblk.so.*
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md


%package -n libpmemblk-devel
Summary: Development files for the Persistent Memory Resident Array of Blocks library
Requires: libpmemblk = %{version}-%{release}
Requires: libpmem-devel = %{version}-%{release}
%description -n libpmemblk-devel
The libpmemblk implements a pmem-resident array of blocks, all the same
size, where a block is updated atomically with respect to power
failure or program interruption (no torn blocks).

For example, a program keeping a cache of fixed-size objects in pmem
might find this library useful. This library is provided for cases
requiring large arrays of objects at least 512 bytes each. Most
developers will find higher level libraries like libpmemobj to be
more generally useful.

%files -n libpmemblk-devel
%{_libdir}/libpmemblk.so
%{_libdir}/pkgconfig/libpmemblk.pc
%{_includedir}/libpmemblk.h
%{_mandir}/man7/libpmemblk.7.gz
%{_mandir}/man5/poolset.5.gz
%{_mandir}/man3/pmemblk_*.3.gz
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md


%package -n libpmemblk-debug
Summary: Debug variant of the Persistent Memory Resident Array of Blocks library
Requires: libpmemblk = %{version}-%{release}
%description -n libpmemblk-debug
The libpmemblk implements a pmem-resident array of blocks, all the same
size, where a block is updated atomically with respect to power
failure or program interruption (no torn blocks).

This sub-package contains debug variant of the library, providing
run-time assertions and trace points. The typical way to access the
debug version is to set the environment variable LD_LIBRARY_PATH to
/usr/lib64/pmdk_debug.

%files -n libpmemblk-debug
%dir %{_libdir}/pmdk_debug
%{_libdir}/pmdk_debug/libpmemblk.so
%{_libdir}/pmdk_debug/libpmemblk.so.*
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md


%package -n libpmemlog
Summary: Persistent Memory Resident Log File library
Requires: libpmem >= %{version}-%{release}
%description -n libpmemlog
The libpmemlog library provides a pmem-resident log file. This is
useful for programs like databases that append frequently to a log
file.

%files -n libpmemlog
%{_libdir}/libpmemlog.so.*
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md


%package -n libpmemlog-devel
Summary: Development files for the Persistent Memory Resident Log File library
Requires: libpmemlog = %{version}-%{release}
Requires: libpmem-devel = %{version}-%{release}
%description -n libpmemlog-devel
The libpmemlog library provides a pmem-resident log file. This
library is provided for cases requiring an append-mostly file to
record variable length entries. Most developers will find higher
level libraries like libpmemobj to be more generally useful.

%files -n libpmemlog-devel
%{_libdir}/libpmemlog.so
%{_libdir}/pkgconfig/libpmemlog.pc
%{_includedir}/libpmemlog.h
%{_mandir}/man7/libpmemlog.7.gz
%{_mandir}/man5/poolset.5.gz
%{_mandir}/man3/pmemlog_*.3.gz
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md


%package -n libpmemlog-debug
Summary: Debug variant of the Persistent Memory Resident Log File library
Requires: libpmemlog = %{version}-%{release}
%description -n libpmemlog-debug
The libpmemlog library provides a pmem-resident log file. This
library is provided for cases requiring an append-mostly file to
record variable length entries. Most developers will find higher
level libraries like libpmemobj to be more generally useful.

This sub-package contains debug variant of the library, providing
run-time assertions and trace points. The typical way to access the
debug version is to set the environment variable LD_LIBRARY_PATH to
/usr/lib64/pmdk_debug.

%files -n libpmemlog-debug
%dir %{_libdir}/pmdk_debug
%{_libdir}/pmdk_debug/libpmemlog.so
%{_libdir}/pmdk_debug/libpmemlog.so.*
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md


%package -n libpmemobj
Summary: Persistent Memory Transactional Object Store library
Requires: libpmem >= %{version}-%{release}
%description -n libpmemobj
The libpmemobj library provides a transactional object store,
providing memory allocation, transactions, and general facilities for
persistent memory programming.

%files -n libpmemobj
%{_libdir}/libpmemobj.so.*
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md


%package -n libpmemobj-devel
Summary: Development files for the Persistent Memory Transactional Object Store library
Requires: libpmemobj = %{version}-%{release}
Requires: libpmem-devel = %{version}-%{release}
%description -n libpmemobj-devel
The libpmemobj library provides a transactional object store,
providing memory allocation, transactions, and general facilities for
persistent memory programming. Developers new to persistent memory
probably want to start with this library.

%files -n libpmemobj-devel
%{_libdir}/libpmemobj.so
%{_libdir}/pkgconfig/libpmemobj.pc
%{_includedir}/libpmemobj.h
%dir %{_includedir}/libpmemobj
%{_includedir}/libpmemobj/*.h
%{_mandir}/man7/libpmemobj.7.gz
%{_mandir}/man5/poolset.5.gz
%{_mandir}/man3/pmemobj_*.3.gz
%{_mandir}/man3/pobj_*.3.gz
%{_mandir}/man3/oid_*.3.gz
%{_mandir}/man3/toid*.3.gz
%{_mandir}/man3/direct_*.3.gz
%{_mandir}/man3/d_r*.3.gz
%{_mandir}/man3/tx_*.3.gz
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md


%package -n libpmemobj-debug
Summary: Debug variant of the Persistent Memory Transactional Object Store library
Requires: libpmemobj = %{version}-%{release}
%description -n libpmemobj-debug
The libpmemobj library provides a transactional object store,
providing memory allocation, transactions, and general facilities for
persistent memory programming. Developers new to persistent memory
probably want to start with this library.

This sub-package contains debug variant of the library, providing
run-time assertions and trace points. The typical way to access the
debug version is to set the environment variable LD_LIBRARY_PATH to
/usr/lib64/pmdk_debug.

%files -n libpmemobj-debug
%dir %{_libdir}/pmdk_debug
%{_libdir}/pmdk_debug/libpmemobj.so
%{_libdir}/pmdk_debug/libpmemobj.so.*
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md


%package -n libpmempool
Summary: Persistent Memory pool management library
Requires: libpmem >= %{version}-%{release}
%description -n libpmempool
The libpmempool library provides a set of utilities for off-line
administration, analysis, diagnostics and repair of persistent memory
pools created by libpmemlog, libpmemblk and libpmemobj libraries.

%files -n libpmempool
%{_libdir}/libpmempool.so.*
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md


%package -n libpmempool-devel
Summary: Development files for Persistent Memory pool management library
Requires: libpmempool = %{version}-%{release}
Requires: libpmem-devel = %{version}-%{release}
%description -n libpmempool-devel
The libpmempool library provides a set of utilities for off-line
administration, analysis, diagnostics and repair of persistent memory
pools created by libpmemlog, libpmemblk and libpmemobj libraries.

%files -n libpmempool-devel
%{_libdir}/libpmempool.so
%{_libdir}/pkgconfig/libpmempool.pc
%{_includedir}/libpmempool.h
%{_mandir}/man7/libpmempool.7.gz
%{_mandir}/man5/poolset.5.gz
%{_mandir}/man3/pmempool_*.3.gz
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md


%package -n libpmempool-debug
Summary: Debug variant of the Persistent Memory pool management library
Requires: libpmempool = %{version}-%{release}
%description -n libpmempool-debug
The libpmempool library provides a set of utilities for off-line
administration, analysis, diagnostics and repair of persistent memory
pools created by libpmemlog, libpmemblk and libpmemobj libraries.

This sub-package contains debug variant of the library, providing
run-time assertions and trace points. The typical way to access the
debug version is to set the environment variable LD_LIBRARY_PATH to
/usr/lib64/pmdk_debug.

%files -n libpmempool-debug
%dir %{_libdir}/pmdk_debug
%{_libdir}/pmdk_debug/libpmempool.so
%{_libdir}/pmdk_debug/libpmempool.so.*
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md


%package -n pmempool
Summary: Utilities for Persistent Memory
Requires: libpmem >= %{version}-%{release}
Requires: libpmemlog >= %{version}-%{release}
Requires: libpmemblk >= %{version}-%{release}
Requires: libpmemobj >= %{version}-%{release}
Requires: libpmempool >= %{version}-%{release}
Obsoletes: nvml-tools < %{version}-%{release}
%description -n pmempool
The pmempool is a standalone utility for management and off-line analysis
of Persistent Memory pools created by PMDK libraries. It provides a set
of utilities for administration and diagnostics of Persistent Memory pools.
The pmempool may be useful for troubleshooting by system administrators
and users of the applications based on PMDK libraries.

%files -n pmempool
%{_bindir}/pmempool
%{_mandir}/man1/pmempool.1.gz
%{_mandir}/man1/pmempool-*.1.gz
%config(noreplace) %{_sysconfdir}/bash_completion.d/pmempool
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md


%if %{with ndctl}

%package -n daxio
Summary: Perform I/O on Device DAX devices or zero a Device DAX device
Requires: libpmem >= %{version}-%{release}
%description -n daxio
The daxio utility performs I/O on Device DAX devices or zero
a Device DAX device.  Since the standard I/O APIs (read/write) cannot be used
with Device DAX, data transfer is performed on a memory-mapped device.
The daxio may be used to dump Device DAX data to a file, restore data from
a backup copy, move/copy data to another device or to erase data from
a device.

%files -n daxio
%{_bindir}/daxio
%{_mandir}/man1/daxio.1.gz
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md

# _with_ndctl
%endif

%if %{with pmemcheck}
%package -n pmreorder
Summary: Consistency Checker for Persistent Memory
Requires: python3
%description -n pmreorder
The pmreorder tool is a collection of python scripts designed to parse
and replay operations logged by pmemcheck - a persistent memory checking tool.
Pmreorder performs the store reordering between persistent memory barriers -
a sequence of flush-fence operations. It uses a consistency checking routine
provided in the command line options to check whether files are in a consistent state.

%files -n pmreorder
%{_bindir}/pmreorder
%{_datadir}/pmreorder/*.py
%{_mandir}/man1/pmreorder.1.gz
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md

# _with_pmemcheck
%endif

%prep
%setup -q -n pmdk-%{upstreamversion}
%patch0 -p1
%patch1 -p1


%build
# This package calls binutils components directly and would need to pass
# in flags to enable the LTO plugins
# Disable LTO
%define _lto_cflags %{nil}

# For debug build default flags may be overriden to disable compiler
# optimizations.
CFLAGS="%{optflags}" \
LDFLAGS="%{?__global_ldflags}" \
make %{?_smp_mflags} NORPATH=1 DOC=n


# Override LIB_AR with empty string to skip installation of static libraries
%install
make install DESTDIR=%{buildroot} \
	DOC=n \
	LIB_AR= \
	prefix=%{_prefix} \
	libdir=%{_libdir} \
	includedir=%{_includedir} \
	mandir=%{_mandir} \
	bindir=%{_bindir} \
	sysconfdir=%{_sysconfdir} \
	docdir=%{_docdir}
mkdir -p %{buildroot}%{_datadir}/pmdk
cp utils/pmdk.magic %{buildroot}%{_datadir}/pmdk/
mkdir -p %{buildroot}%{_mandir}
(cd %{buildroot}%{_mandir}; tar xzvf %{SOURCE1})


%check
%if 0%{?_skip_check} == 1
	echo "Check skipped"
%else
	echo "PMEM_FS_DIR=/tmp"                  > src/test/testconfig.sh
	echo "PMEM_FS_DIR_FORCE_PMEM=1"         >> src/test/testconfig.sh
	echo 'TEST_BUILD="debug nondebug"'      >> src/test/testconfig.sh
	echo "TM=1"                             >> src/test/testconfig.sh

	echo "config = {"                        > src/test/testconfig.py
	echo "  'pmem_fs_dir': '/tmp',"         >> src/test/testconfig.py
	echo "  'fs_dir_force_pmem': 1,"        >> src/test/testconfig.py
	echo "  'build': ['debug', 'release']," >> src/test/testconfig.py
	echo "  'tm': 1,"                       >> src/test/testconfig.py
	echo "  'test_type': 'check',"          >> src/test/testconfig.py
	echo "  'fs': 'all',"                   >> src/test/testconfig.py
	echo "  'unittest_log_level': 1,"       >> src/test/testconfig.py
	echo "  'keep_going': False,"           >> src/test/testconfig.py
	echo "  'timeout': '30m',"              >> src/test/testconfig.py
	echo "  'dump_lines': 30,"              >> src/test/testconfig.py
	echo "  'force_enable': None,"          >> src/test/testconfig.py
	echo "  'device_dax_path': [],"         >> src/test/testconfig.py
	echo "  'granularity': 'cacheline',"    >> src/test/testconfig.py
	echo "  'enable_admin_tests': False,"   >> src/test/testconfig.py
	echo "  'fail_on_skip': False,"         >> src/test/testconfig.py
	echo "  'cacheline_fs_dir': '/tmp',"    >> src/test/testconfig.py
	echo "  'force_cacheline': True,"       >> src/test/testconfig.py
	echo "  'granularity': 'cacheline',"    >> src/test/testconfig.py
	echo "}"                                >> src/test/testconfig.py

	rm -f src/test/obj_sync/TEST7

	make pycheck
	make check
%endif

%ldconfig_scriptlets   -n libpmem
%ldconfig_scriptlets   -n libpmem2
%ldconfig_scriptlets   -n libpmemblk
%ldconfig_scriptlets   -n libpmemlog
%ldconfig_scriptlets   -n libpmemobj
%ldconfig_scriptlets   -n libpmempool

%if 0%{?__debug_package} == 0
%debug_package
%endif


%changelog
* Tue Oct 18 2022 Bryan Gurney <bgurney@redhat.com > 1.12.1-1
- Update to PMDK version 1.12.1
- Related: rhbz#2111431

* Mon Feb 07 2022 Bryan Gurney <bgurney@redhat.com> - 1.10.1-2
- Use DDEBUG in Makefile.inc instead of DEBUG_CFLAGS
- Related: rhbz#2044882

* Thu Oct 14 2021 Bryan Gurney <bgurney@redhat.com> - 1.10.1-1
- Update to PMDK version 1.10.1
- Related: rhbz#1874208
- Remove BuildRequires line for libfabric-devel
- Related: rhbz#2009502

* Mon Oct 04 2021 Bryan Gurney <bgurney@redhat.com> - 1.10-11
- Do not generate librpmem man pages
- Related: rhbz#2002998

* Thu Sep 16 2021 Bryan Gurney <bgurney@redhat.com> - 1.10-10
- Do not build librpmem packages
- Related: rhbz#2002998

* Mon Aug 09 2021 Mohan Boddu <mboddu@redhat.com> - 1.10-9
- Rebuilt for IMA sigs, glibc 2.34, aarch64 flags
  Related: rhbz#1991688

* Mon Aug 02 2021 Bryan Gurney <bgurney@redhat.com> - 1.10-8.el9
- Supersede uninitialized value patch with upstream version
- Add upstream patch: common: fix mismatch between prototype and body
- Makefile: bypass check-doc in check target
- Related: rhbz#1985096

* Fri Jul 30 2021 Bryan Gurney <bgurney@redhat.com> - 1.10.7-el9
- Remove BuildRequires line for libunwind.devel
- Resolves: rhbz#1984766

* Wed Jun 16 2021 Jeff Moyer <jmoyer@redhat.com> - 1.10-6.el9
- Build man pages outside of the rpm.
- Resolves: rhbz#1943530

* Mon Apr 26 2021 Jeff Moyer <jmoyer@redhat.com> - 1.10-5
- Don't run %check on the build infrastructure.
- Resolves: rhbz#1951273

* Fri Apr 16 2021 Mohan Boddu <mboddu@redhat.com> - 1.10-4
- Rebuilt for RHEL 9 BETA on Apr 15th 2021. Related: rhbz#1947937

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Dec 04 2020 Jeff Law <law@redhat.com> - 1.10-2
- Fix uninitialized variable in tests caught by gcc-11 (again)

* Sat Oct 31 2020 Adam Borowski <kilobyte@angband.pl> - 1.10-1
- Update to PMDK version 1.10
- New set of binary libraries: libpmem2{,-devel,-debug}
- Drop obj_sync/7 test as it randomly fails on ppc64le (to investigate).

* Fri Oct 30 2020 Adam Borowski <kilobyte@angband.pl> - 1.9.2-2
- Second attempt -- retry a transient failure on ppc64le.

* Wed Oct 28 2020 Adam Borowski <kilobyte@angband.pl> - 1.9.2-1
- Update to PMDK version 1.9.2
- Install pmem_ctl(5).

* Fri Oct 2 2020 Adam Borowski <kilobyte@angband.pl> - 1.9.1-1
- Update to PMDK version 1.9.1

* Tue Sep 15 2020 Jeff Law <law@redhat.com> - 1.9-5
- Fix uninitialized variable in tests caught by gcc-11

* Tue Aug 18 2020 Adam Borowski <kilobyte@angband.pl> - 1.9-4
- Fix FTBFS with new binutils.

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.9-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 7 2020 Adam Borowski <kilobyte@angband.pl> - 1.9-1
- Update to PMDK version 1.9
- Drop upstreamed patches.
- Add pandoc and groff to B-Reqs.
- Add required testconfig.py fields.
- Increase test timeout.

* Tue Jun 30 2020 Jeff Law <law@redhat.com> - 1.8-3
Disable LTO

* Wed Feb 26 2020 Marcin Ślusarz <marcin.slusarz@intel.com> - 1.8-2
- Enable PPC64LE packages

* Wed Feb 12 2020 Marcin Ślusarz <marcin.slusarz@intel.com> - 1.8-1
- Update to PMDK version 1.8. This release stops shipping
  libvmem & libvmmalloc. These libraries are now provided by vmem
  package.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Oct 1 2019 Marcin Ślusarz <marcin.slusarz@intel.com> - 1.7-1
- Update to PMDK version 1.7

* Fri Aug 30 2019 Marcin Ślusarz <marcin.slusarz@intel.com> - 1.6.1-1
- Update to PMDK version 1.6.1

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Mar 26 2019 Marcin Ślusarz <marcin.slusarz@intel.com> - 1.6-1
- Update to PMDK version 1.6

* Mon Mar 18 2019 Marcin Ślusarz <marcin.slusarz@intel.com> - 1.6-0.1.rc2
- Update to PMDK version 1.6-rc2

* Fri Mar 08 2019 Marcin Ślusarz <marcin.slusarz@intel.com> - 1.5.1-1
- Update to PMDK version 1.5.1

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Dec 14 2018 Marcin Ślusarz <marcin.slusarz@intel.com> - 1.5-2
- Remove Group: tag and add ownership information for libpmemobj headers
  directory.

* Tue Nov 6 2018 Marcin Ślusarz <marcin.slusarz@intel.com> - 1.5-1
- Update to PMDK version 1.5
  libpmemobj C++ bindings moved to separate package (RHBZ #1647145)
  pmempool convert is now a thin wrapper around pmdk-convert (RHBZ #1647147)

* Fri Aug 17 2018 Marcin Ślusarz <marcin.slusarz@intel.com> - 1.4.2-1
- Update to PMDK version 1.4.2 (RHBZ #1589406)

* Tue Aug 14 2018 Marcin Ślusarz <marcin.slusarz@intel.com> - 1.4.2-0.2.rc1
- Revert package name change

* Tue Aug 14 2018 Marcin Ślusarz <marcin.slusarz@intel.com> - 1.4.2-0.1.rc1
- Update to PMDK version 1.4.2-rc1 (RHBZ #1589406)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Mar 30 2018 Krzysztof Czurylo <krzysztof.czurylo@intel.com> - 1.4-3
- Revert package name change
- Re-enable check

* Thu Mar 29 2018 Krzysztof Czurylo <krzysztof.czurylo@intel.com> - 1.4-2
- Fix issues found by rpmlint

* Thu Mar 29 2018 Krzysztof Czurylo <krzysztof.czurylo@intel.com> - 1.4-1
- Rename NVML project to PMDK
- Update to PMDK version 1.4 (RHBZ #1480578, #1539562, #1539564)

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 27 2018 Krzysztof Czurylo <krzysztof.czurylo@intel.com> - 1.3.1-1
- Update to NVML version 1.3.1 (RHBZ #1480578)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 17 2017 Krzysztof Czurylo <krzysztof.czurylo@intel.com> - 1.3-1
- Update to NVML version 1.3 (RHBZ #1451741, RHBZ #1455216)
- Add librpmem and rpmemd sub-packages
- Force file system to appear as PMEM for make check

* Fri Jun 16 2017 Krzysztof Czurylo <krzysztof.czurylo@intel.com> - 1.2.3-2
- Update to NVML version 1.2.3 (RHBZ #1451741)

* Sat Apr 15 2017 Krzysztof Czurylo <krzysztof.czurylo@intel.com> - 1.2.2-1
- Update to NVML version 1.2.2 (RHBZ #1436820, RHBZ #1425038)

* Thu Mar 16 2017 Krzysztof Czurylo <krzysztof.czurylo@intel.com> - 1.2.1-1
- Update to NVML version 1.2.1 (RHBZ #1425038)

* Tue Feb 21 2017 Krzysztof Czurylo <krzysztof.czurylo@intel.com> - 1.2-3
- Fix compilation under gcc 7.0.x (RHBZ #1424004)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Dec 30 2016 Krzysztof Czurylo <krzysztof.czurylo@intel.com> - 1.2-1
- Update to NVML version 1.2 (RHBZ #1383467)
- Add libpmemobj C++ bindings

* Thu Jul 14 2016 Krzysztof Czurylo <krzysztof.czurylo@intel.com> - 1.1-3
- Add missing package version requirements

* Mon Jul 11 2016 Krzysztof Czurylo <krzysztof.czurylo@intel.com> - 1.1-2
- Move debug variants of the libraries to -debug subpackages

* Sun Jun 26 2016 Krzysztof Czurylo <krzysztof.czurylo@intel.com> - 1.1-1
- NVML 1.1 release
- Update link to source tarball
- Add libpmempool subpackage
- Remove obsolete patches

* Wed Jun 01 2016 Dan Horák <dan[at]danny.cz> - 1.0-3
- switch to ExclusiveArch

* Sun May 29 2016 Krzysztof Czurylo <krzysztof.czurylo@intel.com> - 1.0-2
- Exclude PPC architecture
- Add bug numbers for excluded architectures

* Tue May 24 2016 Krzysztof Czurylo <krzysztof.czurylo@intel.com> - 1.0-1
- Initial RPM release

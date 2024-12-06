# For now -- since C code (built with clang) and
# Fortran code (built with gfortran) are linked
# together, LTO object files don't work
%global _disable_lto 0

%define	major 5
%define	libname		%mklibname %{name}
%define	develname	%mklibname %{name} -d
%define oldlibname	%mklibname %{name} 5

%bcond cuda	0
%bcond fortran	1
%bcond lapack	1
%bcond pthread	1

# The cmake files in this package have a load of optional dependencies
# (with checks for them) on things we don't currently ship:
# CALIPER
# Ginkgo
# Kokkos
# KokkosKernels
# RAJA
%define __requires_exclude_from ^%{_libdir}/cmake

# BLAS lib
%global blaslib flexiblas

Summary:	SUite of Nonlinear and DIfferential/ALgebraic Equation Solvers
Name:		sundials
Version:	7.1.1
Release:	1
License:	BSD
Group:		Sciences/Computer science
URL:		https://computation.llnl.gov/projects/%{name}
Source0:	https://github.com/LLNL/%{name}/releases/download/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	gcc-gfortran
BuildRequires:	gomp-devel
BuildRequires:	openmpi-devel
BuildRequires:	pkgconfig(%{blaslib})
%ifarch %{ix86} x86_64
BuildRequires:	quadmath-devel
%endif
BuildRequires:	suitesparse-devel

%description
SUNDIALS is a SUite of Nonlinear and DIfferential/ALgebraic equation
Solvers. It consists of the following six solvers:
  - CVODE solves initial value problems for ordinary differential
          equation (ODE) systems;
  - CVODES solves ODE systems and includes sensitivity analysis
           capabilities (forward and adjoint);
  - ARKODE solves initial value ODE problems with additive
           Runge-Kutta methods, include support for IMEX methods;
  - IDA solves initial value problems for differential-algebraic
        equation (DAE) systems;
  - IDAS solves DAE systems and includes sensitivity analysis
         capabilities (forward and adjoint); 
  - KINSOL solves nonlinear algebraic systems.

#---------------------------------------------------------------------------

%package -n %{libname}
Summary:	SUite of Nonlinear and DIfferential/ALgebraic Equation Solvers
Group:		System/Libraries
%rename %oldlibname

%description -n %{libname}
SUNDIALS is a SUite of Nonlinear and DIfferential/ALgebraic equation
Solvers. It consists of the following six solvers:
  - CVODE solves initial value problems for ordinary differential
          equation (ODE) systems;
  - CVODES solves ODE systems and includes sensitivity analysis
           capabilities (forward and adjoint);
  - ARKODE solves initial value ODE problems with additive
           Runge-Kutta methods, include support for IMEX methods;
  - IDA solves initial value problems for differential-algebraic
        equation (DAE) systems;
  - IDAS solves DAE systems and includes sensitivity analysis
         capabilities (forward and adjoint); 
  - KINSOL solves nonlinear algebraic systems.

%files -n %{libname}
%{_libdir}/*.so.*

#---------------------------------------------------------------------------

%package -n %{develname}
Summary:	Development files for the SUNDIALS libraries
Group:		Development/Other
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}

%description -n %{develname}
This package contains development files for %{name}.

%files -n %{develname}
%license LICENSE
%doc README.md
%{_includedir}/arkode
%{_includedir}/cvode
%{_includedir}/cvodes
%{_includedir}/ida
%{_includedir}/idas
%{_includedir}/kinsol
%{_includedir}/nvector
%{_includedir}/sunadaptcontroller
%{_includedir}/sundials
%{_includedir}/sunlinsol
%{_includedir}/sunmatrix
%{_includedir}/sunmemory
%{_includedir}/sunnonlinsol
%if %{with fortran}
%{_includedir}/*.mod
%endif
%{_libdir}/lib%{name}_*.so
%{_libdir}/cmake/%{name}/*.cmake
%{_datadir}/%{name}/examples

#---------------------------------------------------------------------------

%prep
%autosetup -p1

%build
export FC=gfortran

%cmake -Wno-dev \
	-DBUILD_STATIC_LIBS:BOOL=OFF \
	-DBUILD_FORTRAN77_INTERFACE:BOOL=OFF \
	-DBUILD_FORTRAN_MODULE_INTERFACE:BOOL=%{?with_fortran:ON}%{!?with_fortran:OFF} \
	-DFortran_INSTALL_MODDIR:PATH=%{_includedir} \
	-DENABLE_MPI:BOOL=OFF \
	-DENABLE_OPENMP:BOOL=ON \
	-DENABLE_PTHREAD:BOOL=%{?with_pthread:ON}%{!?with_pthread:OFF} \
	-DENABLE_CUDA:BOOL=%{?with_cuda:ON}%{!?with_cuda:OFF} \
	-DENABLE_LAPACK:BOOL=%{?with_lapack:ON}%{!?with_lapack:OFF} \
	-DENABLE_KLU:BOOL=ON \
	-DKLU_INCLUDE_DIR:PATH=%{_includedir}/suitesparse \
	-DKLU_LIBRARY_DIR:PATH=%{_libdir} \
	-DEXAMPLES_INSTALL_PATH:PATH=%{_datadir}/%{name}/examples \
	-DEXAMPLES_ENABLE_CXX:BOOL=ON \
	-DCMAKE_C_STANDARD=17 \
	-GNinja
%ninja_build

%install
%ninja_install -C build

rm %{buildroot}%{_includedir}/sundials/LICENSE


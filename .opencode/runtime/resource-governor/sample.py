"""Bounded, read-only OS metrics. No commands, paths or environment are exported."""
import ctypes
import json
import os
from pathlib import Path
import subprocess
import sys


def sysctl(name):
    libc = ctypes.CDLL('/usr/lib/libSystem.B.dylib', use_errno=True)
    value = ctypes.c_uint64()
    size = ctypes.c_size_t(ctypes.sizeof(value))
    if libc.sysctlbyname(name.encode(), ctypes.byref(value), ctypes.byref(size), None, 0):
        raise OSError(ctypes.get_errno(), 'sysctl unavailable')
    return value.value


def sample(pids):
    if len(pids) > 64:
        raise ValueError('PID sample bound exceeded')
    if sys.platform == 'darwin':
        used, limit, physical = (sysctl(k) for k in ('kern.num_files', 'kern.maxfiles', 'hw.memsize'))
        libproc = ctypes.CDLL('/usr/lib/libproc.dylib', use_errno=True)
        groups = pids[1:]
        expanded = set(pids)
        for group in groups:
            buf = (ctypes.c_int * 65)()
            size = libproc.proc_listpids(2, group, buf, ctypes.sizeof(buf))
            if size >= ctypes.sizeof(buf):
                raise OSError('Managed group exceeds PID sample bound')
            expanded.update(pid for pid in buf[:max(0, size // 4)] if pid > 0)
        if len(expanded) > 64:
            raise OSError('Managed tree exceeds PID sample bound')
        pids = sorted(expanded)
        def descriptors(pid):
            # PROC_PIDLISTFDS: struct proc_fdinfo = int32 fd + uint32 type.
            size = libproc.proc_pidinfo(pid, 1, 0, None, 0)
            if size <= 0 or size > 8 * 1048576:
                return None
            buf = ctypes.create_string_buffer(size + 8 * 32)
            count = libproc.proc_pidinfo(pid, 1, 0, buf, len(buf))
            return count // 8 if 0 < count < len(buf) else None
    elif sys.platform.startswith('linux'):
        allocated, unused, limit = map(int, Path('/proc/sys/fs/file-nr').read_text().split())
        used = allocated - unused
        physical = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')
        def descriptors(pid):
            try:
                return len(os.listdir('/proc/%s/fd' % pid))
            except OSError:
                return None
    else:
        raise OSError('System FD monitoring unsupported on this platform')
    # One bounded-output command for known PIDs; no full-system process/lsof scan.
    processes = []
    if pids:
        result = subprocess.run(['ps', '-p', ','.join(map(str, pids)), '-o', 'pid=,ppid=,pgid=,rss=,vsz=,stat='],
                                capture_output=True, text=True, timeout=1)
        for line in result.stdout.splitlines():
            pid, parent, group, rss, virtual, state = line.split()
            processes.append(dict(pid=int(pid), parentPID=int(parent), group=int(group),
                                  rss=int(rss) * 1024, virtual=int(virtual) * 1024,
                                  zombie=state.startswith('Z'), fd=descriptors(int(pid))))
    return dict(systemFD=used, systemLimit=limit, physicalMemory=physical, processes=processes,
                systemMemoryPressure=None, allocatorMemory=None)


if __name__ == '__main__':
    print(json.dumps(sample([int(p) for p in sys.argv[1:]])))

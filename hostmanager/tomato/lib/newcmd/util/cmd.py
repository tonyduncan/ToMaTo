import subprocess, os
from .. import Error
from daemon import Daemon

DEVNULL = open("/dev/null", "w")


class CommandError(Error):
	CODE_EXECUTE = "cmd.execute"



def spawn(cmd, stdout=DEVNULL, cwd=None):
	proc = subprocess.Popen(cmd, cwd=cwd, stdout=stdout, stderr=subprocess.STDOUT, close_fds=True)
	return proc.pid


def spawnDaemon(cmd, cwd=None):
	class Dummy(Daemon):
		def run(self):
			DEVNULL = open("/dev/null", "w")
			proc = subprocess.Popen(cmd, cwd=cwd, stdout=DEVNULL, stderr=subprocess.STDOUT, close_fds=False)
			self.send(str(proc.pid))

	dummy = Dummy()
	dummy.start()
	pid = int(dummy.recv(16))
	return pid


def run(cmd, ignoreErr=False, input=None, cwd=None):  # @ReservedAssignment
	stderr = DEVNULL if ignoreErr else subprocess.STDOUT
	stdin = subprocess.PIPE if input else None
	proc = subprocess.Popen(cmd, cwd=cwd, stdin=stdin, stdout=subprocess.PIPE, stderr=stderr, shell=False,
		close_fds=True)
	output = proc.communicate(input)[0]
	error = proc.returncode
	if error:
		raise CommandError(CommandError.CODE_EXECUTE, "Error executing command",
			{"cmd": cmd, "error": error, "output": output})
	return output


def lookup(prog):
	for dir_ in os.environ['PATH'].split(os.pathsep):
		path = os.path.join(dir_, prog)
		if os.path.exists(path):
			return path


def exists(prog):
	return bool(lookup(prog))
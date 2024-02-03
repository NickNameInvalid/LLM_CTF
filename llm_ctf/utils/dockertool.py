import subprocess
class DockerHelper:
    def __init__(self, container_name):
        self.container = container_name
    
    def docker_start(self):
        raise NotImplementedError

    def docker_stop(self):
        raise NotImplementedError
    
    def docker_copy(self, docker_id, src, dest):
        raise NotImplementedError
    
    def docker_exec(self, cmd):
        # subprocess.run(['sudo', 'docker', 'run','--rm', '-it', '-v', '$PWD:/opt/exp', self.container, cmd], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=5)
        # p = subprocess.run(['sudo', 'docker', 'run','--rm', '-it', '-v', '$PWD:/opt/exp', self.container, cmd], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=5)
        # res: str = str('\n' + p.stdout.decode("utf-8"))
        try:
            p = subprocess.run(['sudo', 'docker', 'run','--rm', '-it', '-v', '$PWD:/opt/exp', self.container, cmd], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=5)
            res: str = str('\n' + p.stdout.decode("utf-8"))
        except Exception as e:
            print(f"Validation failed, solver cannot be executed or solver execution error")
            return self.valid







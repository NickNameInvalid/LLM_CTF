class DockerHelper:
    def __init__(self):
        raise NotImplementedError
    
    def docker_start(self):
        raise NotImplementedError
    
    def docker_stop(self):
        raise NotImplementedError
    
    def docker_copy(self, docker_id, src, dest):
        raise NotImplementedError
    
    def docker_exec(self):
        raise NotImplementedError
    
    
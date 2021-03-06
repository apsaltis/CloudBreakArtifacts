import sys, os, pwd, signal, time, shutil
from subprocess import *
from resource_management import *

class DemoControl(Script):
  def install(self, env):
    self.configure(env)
    import params
  
    if not os.path.exists(params.install_dir):  
        os.makedirs(params.install_dir)
    os.chdir(params.install_dir)
    if not os.path.exists(params.install_dir+'/sam-custom-extensions'):
        Execute('git clone ' + params.sam_extensions_download_url)
    if not os.path.exists(params.install_dir+'/Data-Loader'):
        Execute('wget -O simulator.zip '+params.download_url)
        Execute('unzip simulator.zip')
        os.chdir(params.install_dir+'/Data-Loader')
        Execute('tar -zxvf routes.tar.gz')
    os.chdir(params.install_dir)
    Execute(params.install_dir+'/CloudBreakArtifacts/recipes/trucking-demo-sam-install.sh')

  def start(self, env):
    self.configure(env)
    import params
    Execute('echo Start Simulation')
    Execute('nohup java -cp '+params.install_dir+'/Data-Loader/data-loader-jar-with-dependencies.jar hortonworks.hdp.refapp.trucking.simulator.SimulationRegistrySerializerRunnerApp 20000 hortonworks.hdp.refapp.trucking.simulator.impl.domain.transport.Truck hortonworks.hdp.refapp.trucking.simulator.impl.collectors.FileEventWithSchemaIdCollector 1 '+params.install_dir+'/Data-Loader/routes/midwest/ 10000 /tmp/truck-sensor-data/telemetry-device-4.txt http://localhost:7788/api/v1 ALL_STREAMS & 2>&1 & ')
    Execute('ps -ef|grep "Data-Loader/data-loader-jar-with-dependencies.jar"| grep -v grep| awk \'{print $2}\' > /var/run/TruckSim.pid')
    
  def stop(self, env):
    self.configure(env)
    import params
    Execute('echo Stop Simulation')
    Execute ('kill -9 `ps -ef|grep "Data-Loader/data-loader-jar-with-dependencies.jar"| grep -v grep| awk \'{print $2}\'` >/dev/null 2>&1') 
    Execute ('rm -f /var/run/TruckSim.pid')
    
  def status(self, env):
    import params
    env.set_params(params)
    check_process_status('/var/run/TruckSim.pid')
    
  def configure(self, env):
    import params
    env.set_params(params)

if __name__ == "__main__":
  DemoControl().execute()

import sys
import os
import py_compile
import argparse
import cv2
import tools

parser = argparse.ArgumentParser()
parser.add_argument("user_server", help="user@server")
parser.add_argument("action", help="action", choices=['run',
                                                      'stop',
                                                      'install',
                                                      'reboot',
                                                      'snapshot'])

opt = parser.parse_args()

LOCAL_DEST = 'port'
REMOTE_DEST = 'i-drive'


def remote_run(user,server,cmd, run_in_dir=False):
    "run the  remote command 'cmd' on user@server using ssh"


    if run_in_dir:
        cmd = "(cd ~/%s; %s)"%(REMOTE_DEST, cmd)

    rcmd = "ssh %s@%s '%s'"%(user,server,cmd)

        
    print rcmd
    
    os.system(rcmd)
    

def remote_copy(user,server,src_file,dest_file,upload=True):
    "copy src_file to dest_file on user@server using scp"

    if upload:
        # upload to device
        rcmd = "scp %s %s@%s:%s"%(src_file,user,server,dest_file)
    else:
        # download from device
        rcmd = "scp %s@%s:%s %s"%(user,server,src_file,dest_file)
    print rcmd
    os.system(rcmd)



def install_startup(user,server,opt):
    "install startup scripts on the user@server"


    remote_copy(user,server,'startup.sh', '~/.startup')
    remote_run(user,server, 'sudo chmod a+x ~/.startup')

    # create startup directories
    #remote_run(user, server, "mkdir -p ~/.config")
    #remote_run(user, server, "mkdir -p ~/.config/autostart/")
        
    #remote_copy(user,server,'i-drive.desktop', '~/.config/autostart/')

    
    
    

    
def install(user, server, opt):
    "Install i-drive software on remote server"

    print 'Installing on %s@%s ...'%(user,server)

    
    # create i-drive directory
    remote_run(user, server, "mkdir -p %s"%os.path.join('~', REMOTE_DEST))

    
    
    source_list = ['main.py',
                   'capture.py',
                   'FCW.py',
                   'filters.py',
                   'tools.py',
                   'audio.py',
                   'gui.py',
                   'path.py',
                   'store.py',
                   'options.py',
                   'take_snapshot.py',
                   'calibration.py',
                   'stop.py',
                   'update_store_format.py',
                   'data_streamer.py',
                   'delete_corrupted.py',
                   'tracking.py',
    ]

    
    
    local_dest_list = [os.path.join(LOCAL_DEST, source + 'c') for source in source_list]

    remote_dest_list = [os.path.join('~', REMOTE_DEST, source + 'c') for source in source_list]

    
    for source, ldest in zip(source_list,local_dest_list):
        py_compile.compile(source, ldest)

        
    # copy the .pyc files to remote server
    remote_copy(user,server,os.path.join(LOCAL_DEST,'*.pyc'), os.path.join('~', REMOTE_DEST))
    
    # copy the cascade to remote server
    remote_copy(user,server,'car_cascade.xml run_all.sh',os.path.join('~', REMOTE_DEST))

    # copy the logo to remote server
    remote_copy(user,server,'rahbin.png',os.path.join('~', REMOTE_DEST))

    calib_dir = os.path.join('~', REMOTE_DEST, 'calib')
    
    # create calibration directory 
    remote_run(user, server, "mkdir -p %s"%calib_dir)
    
    # copy calibration files
    #remote_copy(user,server,'calib/*.cpp calib/*.h calib/Makefile calib/settings.yaml ', calib_dir)
    remote_copy(user,server,'calib/extrinsics.xml', calib_dir)

    data_dir = os.path.join('~', 'data')
    
    # create data directory 
    remote_run(user, server, "mkdir -p %s"%data_dir)

    # create port directory
    remote_run(user, server, "mkdir -p ~/i-drive/port")


    # install simd files
    remote_run(user, server, "mkdir -p simd", True)
    remote_copy(user,server,'simd/arm/simd/simd.so', '~/i-drive/simd')
    remote_copy(user,server,'simd/arm/simd/__init__.py', '~/i-drive/simd')

    # install startup files
    install_startup(user,server,opt)
    

    
    
    

    
            

def run(user, server, opt):
    "Run i-drive software on remote server"

    print 'Running on %s@%s ...'%(user,server)

    remote_run(user,server,'(~/.startup &)')
    


def stop(user, server, opt):
    "Stop i-drive software on remote server"
    
    print 'Stopping on %s ...'%(server,)

    #remote_run(user,server,"sudo kill -9 `ps ax | grep bash | grep .startup | awk '{print $1}'`")

    remote_run(user,server, 'sudo python stop.pyc', True)

    #os.system(cmd)


def reboot(user, server, opt):
    "Reboots i-drive"

    print 'rebooting %s ...'%(server,)
    cmd = "ssh %s@%s 'sudo reboot'"%(user,server)
    print cmd
    os.system(cmd)


def snapshot(user,server,opt):
    "Takes a snapshot and returns image"

    # take a snapshot and save to remote directory "port"
    remote_run(user,server,'python take_snapshot.pyc', True)

    # download snapshot from remote port to local port
    remote_copy(user,server,
                os.path.join('~', REMOTE_DEST, "port", "snapshot.jpg"), 'port',
                upload=False)


    I = cv2.imread('port/snapshot.jpg')

    cv2.imshow('snapshot', I)
    cv2.waitKey()

    

    

    

if __name__ == '__main__':

   
    user,server = opt.user_server.strip().split('@')

    action_func = eval(opt.action)

    action_func(user,server, opt)



    


    


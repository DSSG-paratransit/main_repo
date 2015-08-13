
# def busReschedule_run(schedule_filename,
                      # accesskey,
                      # secretkey,
                      # broken_run,
                      # path_to_outdir = af.os.path.join(af.os.getcwd(),'data'),
                      # resched_init_time = None,
                      # bookingid = None,
                      # windows = 1800.,
                      # radius = 3.):
import subprocess
args = ['python', 'busRescheduler.py', '/Users/fineiskid/Desktop/DSSG_ffineis/main_repo/Access_Analysis_Rproject/data/output/qc_streaming_DEMO.csv', 'None', 'None', '6020', '/Users/fineiskid/Desktop/DSSG_ffineis/main_repo/Access_Analysis_Rproject/data/output', '11:30', 'None', '1800.', '3.']

p = subprocess.Popen(args)
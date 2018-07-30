from main import *
import filecmp
import time

if __name__ == "__main__":
    # initialize VISUM and load the .ver file
    t0 = time.time()
    if 'Visum' in globals():
        # script
        MAIN_PATH = Visum.GetPath(2)
    else:
        # standalone
        MAIN_PATH = os.path.join(os.getcwd(),"test\\Krakow_PuT_network_2018\\")
        #Visum = win32com.client.Dispatch('Visum.Visum')
        #Visum.LoadVersion(os.path.join(MAIN_PATH,"KRK_PuT_network_2018.ver"))
        #Visum.SetPath(2,MAIN_PATH)
    Visum.Graphic.StopDrawing = True
    main(Visum)
    Visum.Graphic.StopDrawing = False

    for file in os.listdir(MAIN_PATH):
        if file.endswith(".dat"):
            try:
                assert filecmp.cmp(os.path.join(MAIN_PATH, file) , os.path.join(MAIN_PATH,"ref", file))
            except AssertionError as e:
                e.args += (file, "changed")
                raise
    print("Test successful - files are equal, execution time: {}s".format(int(time.time()-t0)))




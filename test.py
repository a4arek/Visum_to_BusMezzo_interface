from main import *

if __name__ == "__main__":
    # initialize VISUM and load the .ver file
    try:
        # from Visum
        Visum
        MAIN_PATH = MAIN_PATH = Visum.GetPath(2)
    except:
        # standalone
        MAIN_PATH = os.getcwd()
        #MAIN_PATH = "E:\BM"
        MAIN_PATH = MAIN_PATH+"\\test\\Krakow_test_I_obw\\"
        Visum = win32com.client.Dispatch('Visum.Visum')
        Visum.LoadVersion(MAIN_PATH+"KRK_test1.ver")
        Visum.SetPath(2,MAIN_PATH)
    Visum.Graphic.StopDrawing = True
    main(Visum)
    Visum.Graphic.StopDrawing = False

    for file in os.listdir(MAIN_PATH):
        if file[:-3] == ".dat":
            assert open(file) == open(MAIN_PATH+"\\ref\\" + file)




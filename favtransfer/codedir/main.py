from portfolio.favtransfer.transfer import ArtistTransfer
import tkinter as tk



AT = ArtistTransfer()



def printy():
    AT.spotify_query(str(e1.get()))
    AT.follower(var1.get())
    master.quit()

master = tk.Tk()
tk.Label(master, text="First Name")
e1 = tk.Entry(master)
e1.grid(row=0, column=0)
var1 = tk.IntVar()
c1 = tk.Checkbutton(master, text='Unfollow?', variable=var1, onvalue=1, offvalue=0)
tk.Button(master,text='Quit',command=master.quit).grid(row=3,column=0,sticky=tk.W,pady=4)
tk.Button(master, text='Show', command=printy).grid(row=3,column=1,sticky=tk.W,pady=4)
master.mainloop()


# pl = 'https://open.spotify.com/playlist/5pVeWznNvTV1wimWkrVYeP?si=6366e2896084421f'




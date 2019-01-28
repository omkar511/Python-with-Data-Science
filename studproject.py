from tkinter import *
from tkinter import messagebox
from tkinter import scrolledtext
import cx_Oracle
from PIL import Image,ImageTk
import bs4
import requests
import datetime
import socket

root1=Tk()
root1.title("Flash")
root1.geometry("500x400+200+200")
root1.after(10000,lambda:root1.destroy())


res=requests.get("https://www.brainyquote.com/quotes_of_the_day.html")
soup=bs4.BeautifulSoup(res.text,'lxml')
quote=soup.find('img',{"class":"p-qotd"})
img_url="https://www.brainyquote.com"+quote['data-img-url']
img_name=datetime.datetime.now().date()
r=requests.get(img_url)
with open(str(img_name)+".jpg",'wb')as f:
	f.write(r.content)



path = str(img_name)+".jpg"
img = ImageTk.PhotoImage(Image.open(path).resize((450,300)))
panel = Label(root1, image = img,height=200)
panel.pack(side = "top", fill = "both", expand = "no")

lblLoc=Label(root1,text="Location :")
lblTemp=Label(root1,text="Temperature :")
lblLoc.place(x=60, y=230)
lblTemp.place(x=300, y=230)


try:
	city='Mumbai'
	socket.create_connection(("www.google.com",80))
	api_address="http://api.openweathermap.org/data/2.5/weather?units=metric"+"&q="+city+"&appid=6bddbf473a3840b52a9fb6084e1fef48"
	wdata=requests.get(api_address).json()
	temp=str(wdata['main']['temp'])
	
except OSError:
	print("check network")


try:
	socket.create_connection(("www.google.com",80))
	res=requests.get("https://ipinfo.io/")
	data=res.json()
	city=data['city']
except OSError:
	print("check network")



lblLoctxt=Label(root1,text=city)
lblTemptxt=Label(root1,text=temp)
lblLoctxt.place(x=120, y=230)
lblTemptxt.place(x=380, y=230)








root1.mainloop()
root=Tk()
root.title("Student Management System")
root.geometry("400x400+200+200")

vist=Toplevel(root)
vist.title("View Student")
vist.geometry("400x400+200+200")
vist.withdraw()
stViewData=scrolledtext.ScrolledText(vist,width=30,height=10)


def f4():
	root.deiconify()
	vist.withdraw()
	stViewData.delete('1.0',END)
btnViewBack=Button(vist,text="back",command=f4)
stViewData.pack()
btnViewBack.pack()

butView=Button(root,text="View")
def f3():
	vist.deiconify()
	root.withdraw()
	con=None
	cursor=None
	
	try:
		con=cx_Oracle.connect('system/abc123')
		print("connected")
		cursor=con.cursor()
		stViewData.configure(state='normal')
		stViewData.delete('1.0',END)
		cursor.execute("select * from student3 order by rno")
		data=cursor.fetchall()
		info=''
		for d in data:
			print("rno ",d[0],"name ",d[1])
			info=info+"rno " +str(d[0])+" name "+d[1]+"\n"
		stViewData.insert(INSERT,info)
		stViewData.configure(state='disabled')
	except cx_Oracle.DatabaseError as e:
		con.rollback()
		print('error',e)
			
	finally:
		if cursor is not None:
			cursor.close()
		if con is not None:
			con.close()
			print("disconnected")
btnView=Button(root,text="View",width=10,command=f3)
adst=Toplevel(root)
adst.title("add student")
adst.geometry('300x300+200+200')
adst.withdraw()

lblRno1=Label(adst,text="enter rno")
entRno1=Entry(adst,bd=5)
lblName1=Label(adst,text="enter name")
entName1=Entry(adst,bd=7)

def f5():
	con=None
	cursor=None
	try:
		con=cx_Oracle.connect('system/abc123')		
		print("connected")
		cursor=con.cursor()
		rno1=int(entRno1.get())
		if rno1<0:
			messagebox.showinfo("","Enter Positive Number")
			entRno1.delete(0,'end')
		else:
			name1=entName1.get()
			if(not name1.isalpha()):
				messagebox.showinfo("","Enter proper name")
				entName1.delete(0,'end')
				entName1.focus()
			else:
				sql="insert into student3 values('%d','%s')"
				args=(rno1,name1)
				cursor.execute(sql % args)
				con.commit()
				print(cursor.rowcount,"records inserted")
				messagebox.showinfo("sucess",str(cursor.rowcount) +" record inserted" )
				entRno1.delete(0,'end')
				entName1.delete(0,'end')
				entRno1.focus()
	except cx_Oracle.DatabaseError as e:
		con.rollback()
		print('error',e)
		messagebox.showerror("faliure","issue" +str(e))
		entRno1.delete(0,'end')
		entRno1.focus()	
	except ValueError:
		messagebox.showerror("Issue","Only Integers allowed")	
		entRno1.delete(0,'end')
		entRno1.focus()	
	finally:
		if cursor is not None:
			cursor.close()
		if con is not None:
			con.close()
			print("disconnected")

btnAddsave=Button(adst,text="save",command=f5)
def f2():
	root.deiconify()
	adst.withdraw()
	entRno1.delete(0,'end')
	entName1.delete(0,'end')
btnAddback=Button(adst,text="Back",command=f2)

lblRno1.pack(pady=10)
entRno1.pack(pady=10)
lblName1.pack(pady=10)
entName1.pack(pady=10)
btnAddsave.pack(pady=10)
btnAddback.pack(pady=10)

def f1():
	adst.deiconify()
	root.withdraw()
	entRno1.focus()
btnAdd=Button(root,text="Add",width=10,command=f1)

btnAdd.pack(pady=20)
btnView.pack(pady=20)

upst=Toplevel(root)
upst.title("Update student")
upst.geometry('300x300+200+200')
upst.withdraw()

lblRno=Label(upst,text="enter rno")
entRno=Entry(upst,bd=5)
lblName=Label(upst,text="enter name")
entName=Entry(upst,bd=7)



def f7():
	con=None
	cursor=None
	try:
		con=cx_Oracle.connect('system/abc123')
				
		print("connected")
		cursor=con.cursor()
		rno=int(entRno.get())
		name=entName.get()
		if(not name.isalpha()):
			messagebox.showinfo("Issue","Enter proper name")
			entName.delete(0,'end')
			entName.focus()
		else:
			sql="update student3 set name='%s' where rno='%d'"
			args=(name,rno)
			cursor.execute(sql % args)
			con.commit()
			print(cursor.rowcount," records updated")
			messagebox.showinfo("success",str(cursor.rowcount) +" record updated" )
			entRno.delete(0,'end')
			entName.delete(0,'end')
			entRno.focus()
	except cx_Oracle.DatabaseError as e:
		con.rollback()
		print('error',e)
		messagebox.showinfo("faliure","issue" +str(e))
		entRno.focus()
	except ValueError:
		messagebox.showerror("Issue","Integers Only")
		entRno.delete(0,'end')
		entRno.focus()
	finally:
		if cursor is not None:
			cursor.close()
		if con is not None:
			con.close()
			print("disconnected")

btnUpdatesave=Button(upst,text="Update",command=f7)
def f8():
	root.deiconify()
	upst.withdraw()
	entRno.delete(0,'end')
	entName.delete(0,'end')
btnUpdateback=Button(upst,text="Back",command=f8)

lblRno.pack(pady=10)
entRno.pack(pady=10)
lblName.pack(pady=10)
entName.pack(pady=10)
btnUpdatesave.pack(pady=10)
btnUpdateback.pack(pady=10)

def f9():
	upst.deiconify()
	root.withdraw()
	entRno.focus()
btnUpdate=Button(root,text="Update",width=10,command=f9)
btnUpdate.pack(pady=20)


dest=Toplevel(root)
dest.title("Update student")
dest.geometry('300x300+200+200')
dest.withdraw()

lblRno2=Label(dest,text="enter rno")
entRno2=Entry(dest,bd=5)



def f10():
	con=None
	cursor=None
	try:
		con=cx_Oracle.connect('system/abc123')
				
		print("connected")
		cursor=con.cursor()
		rno=int(entRno2.get())
		sql="delete from student3 where rno='%d'"
		args=(rno)
		cursor.execute(sql % args)
		con.commit()
		print(cursor.rowcount," record deleted")
		messagebox.showinfo("success",str(cursor.rowcount) +" record deleted" )
		entRno2.delete(0,'end')
		entRno2.focus()
	except cx_Oracle.DatabaseError as e:
		con.rollback()
		print('error',e)
		messagebox.showinfo("faliure","issue" +str(e))
	except ValueError:
		messagebox.showerror("Issue","Integers only")
		entRno2.delete(0,'end')
		entRno2.focus()
	finally:
		if cursor is not None:
			cursor.close()
		if con is not None:
			con.close()
			print("disconnected")

btnDeletesave=Button(dest,text="Delete",command=f10)
def f11():
	root.deiconify()
	dest.withdraw()
	entRno2.delete(0,'end')
btnDeleteback=Button(dest,text="Back",command=f11)

lblRno2.pack(pady=10)
entRno2.pack(pady=10)
btnDeletesave.pack(pady=10)
btnDeleteback.pack(pady=10)

def f12():
	dest.deiconify()
	root.withdraw()
	entRno2.focus()
btnDelete=Button(root,text="Delete",width=10,command=f12)
btnDelete.pack(pady=20)


root.mainloop()







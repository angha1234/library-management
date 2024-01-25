from tkinter import *
from tkinter import ttk, messagebox
import customs as cs
from functools import partial
import pymysql
import credentials as cr


class Management:
    def __init__(self, root):
        self.window = root
        self.window.title("LIBRARY MANAGEMENT SYSTEM")
        self.window.geometry("1070x540")
        self.window.config(bg = "white")

        # Left Frame
        self.frame_1 = Frame(self.window, bg=cs.color_1)
        self.frame_1.place(x=0, y=0, width=740, relheight = 1)
        
        # Right Frame
        self.frame_2 = Frame(self.window, bg = cs.color_2)
        self.frame_2.place(x=740,y=0,relwidth=1, relheight=1)

        # A frame inside the right frame
        self.frame_3 = Frame(self.frame_2, bg= cs.color_2)
        self.frame_3.place(x=0, y=300,relwidth=1, relheight=1)

        # All the Buttons in the frame 2
        self.add_book = Button(self.frame_2, text='ADD BOOK', font=(cs.font_1, 12), bd=2, command=self.AddNewBook,cursor="hand2", bg=cs.color_2,fg=cs.color_3).place(x=40,y=40,width=130)
        self.issue_book = Button(self.frame_2, text='ISSUE BOOK', font=(cs.font_1, 12), bd=2, command=self.GetData_for_IssueBook,cursor="hand2", bg=cs.color_7,fg=cs.color_3).place(x=40,y=100,width=130)
        self.return_book = Button(self.frame_2, text='RETURN BOOK', font=(cs.font_1, 12), bd=2, command=self.ReturnBook,cursor="hand2", bg=cs.color_6,fg=cs.color_3).place(x=40,y=160,width=130)
        self.all_book = Button(self.frame_2, text='ALL BOOKS', font=(cs.font_1, 12), bd=2, command=self.ShowBooks,cursor="hand2", bg=cs.color_2,fg=cs.color_3).place(x=40,y=220,width=130)
        
        self.search_book = Button(self.frame_2, text='SEARCH BOOK', font=(cs.font_1, 12), bd=2, command=self.GetBookNametoSearch,cursor="hand2", bg=cs.color_2,fg=cs.color_3).place(x=180,y=40,width=130)
        self.all_borrow_records = Button(self.frame_2, text='BOOK HOLDERS', font=(cs.font_1, 12), bd=2, command=self.AllBorrowRecords, cursor="hand2", bg=cs.color_2,fg=cs.color_3).place(x=180,y=100,width=130)
        self.clear = Button(self.frame_2, text='CLEAR SCREEN', font=(cs.font_1, 12), bd=2, command=self.ClearScreen,cursor="hand2", bg=cs.color_2,fg=cs.color_3).place(x=180,y=160,width=130)
        self.exit = Button(self.frame_2, text='EXIT', font=(cs.font_1, 12), bd=2, command=self.Exit,cursor="hand2", bg=cs.color_2,fg=cs.color_3).place(x=180,y=220,width=130)
    
    # Function 1: It gets call from 'Function 15' when the user clicks on a record
    def OnSelectedforReturn(self, a):
        self.dlt_record = Button(self.frame_3, text='DELETE', font=(cs.font_1, 12), bd=2, command=self.ReturningBook,cursor="hand2", bg=cs.color_2,fg=cs.color_3).place(x=40,y=0,width=130)
        self.borrow_again = Button(self.frame_3, text='ISSUE AGAIN', font=(cs.font_1, 12), bd=2, command=self.IssueAgain,cursor="hand2", bg=cs.color_2,fg=cs.color_3).place(x=180,y=0,width=130)

    # Function 2: It gets call from 'Function 16' when the user clicks on a record
    def OnSelectedforBorrowRecords(self, a):
        self.dlt_record = Button(self.frame_3, text='DELETE', font=(cs.font_1, 12), bd=2, command=self.ReturningBook,cursor="hand2", bg=cs.color_2,fg=cs.color_3).place(x=40,y=0,width=130)
        self.update_record = Button(self.frame_3, text='UPDATE', font=(cs.font_1, 12), bd=2, command=self.IssueAgain,cursor="hand2", bg=cs.color_2,fg=cs.color_3).place(x=180,y=0,width=130)

    # Function 3: It gets call from 'Function 14' and 'Function 17' when the 
    # user clicks on a record
    def OnSelectedforShowBooks(self, a):
        self.dlt_record = Button(self.frame_3, text='DELETE', font=(cs.font_1, 12), bd=2, command=self.DeleteBook,cursor="hand2", bg=cs.color_2,fg=cs.color_3).place(x=40,y=0,width=130)
        self.update_record = Button(self.frame_3, text='UPDATE', font=(cs.font_1, 12), bd=2, command=self.UpdateBookDetails,cursor="hand2", bg=cs.color_2,fg=cs.color_3).place(x=180,y=0,width=130)

    # Function 4: It gets call from 'Function 3', is used to delete a book
    # but there is a conition. If a book is holding by anyone, the user can't
    # delete the book
    def DeleteBook(self):
        x = self.tree.selection()
        row = self.tree.item(x)['values']
        try:
            status = messagebox.askokcancel('DELETE BOOK', 'DO YOU WANT TO PROCEED?')
            if status == True:
                connection = pymysql.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
                curs = connection.cursor()

                curs.execute("select * from borrow_record where book_id=%s", row[0])
                var = curs.fetchall()

                if len(var) != 0:
                    messagebox.showwarning("CRITICAL WARNING!", "YOU CAN'T DELETE THIS BOOK RECORD")
                else:
                    curs.execute("delete from book_list where book_id=%s",
                    (
                        row[0]
                    ))
                    messagebox.showinfo("SUCCESS!", "THE BOOK RECORD HAS BEEN DELETED")
                    connection.commit()
                    connection.close()
                    self.ClearScreen()
                    self.ShowBooks()
        except Exception as e:
            messagebox.showerror("Error!",f"Error due to {str(e)}",parent=self.window)   

    # Function 5: It gets call from 'Function 1', is used to return a book from the borrower
    def ReturningBook(self):
        x = self.tree_1.selection()
        row = self.tree_1.item(x)['values']
      
        try:
            status = messagebox.askokcancel('RETURNING BOOK', 'DO YOU WANT TO PROCEED?')
            if status == True:
                connection = pymysql.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
                curs = connection.cursor()
                curs.execute("delete from borrow_record where book_id=%s",
                (
                    row[0]
                ))
                curs.execute("select * from book_list where book_id=%s", row[0])
                var = curs.fetchone()

                book_count = var[5]
                book_count += 1

                curs.execute("update book_list set qty=%s where book_id=%s", (book_count, row[0]))

                messagebox.showinfo("SUCCESS!", "THANKS FOR RETURNING THE BOOK!")
                connection.commit()
                connection.close()
                self.ClearScreen()
        except Exception as e:
            messagebox.showerror("ERROR!",f"ERROR DUE TO {str(e)}",parent=self.window)        

    # Function 6: It gets call from 'Function 1', is used to take the date from the
    # user to issue a book again to the borrower. It calls 'Function 7' when the submit button
    # is pressed.
    def IssueAgain(self):
        x = self.tree_1.selection()
        row = self.tree_1.item(x)['values']
    
        self.ClearScreen()

        book_id = Label(self.frame_1, text="BOOK ID", font=(cs.font_2, 15, "bold"), bg=cs.color_1).place(x=130,y=30)
        id = Label(self.frame_1, text=row[0], font=(cs.font_1, 10))
        id.place(x=130,y=60, width=200)

        book_name = Label(self.frame_1, text="BOOK NAME", font=(cs.font_2, 15, "bold"), bg=cs.color_1).place(x=400,y=30)
        bookname = Label(self.frame_1, text=row[1], font=(cs.font_1, 10))
        bookname.place(x=400,y=60, width=200)

        student_roll = Label(self.frame_1, text="STUDENT ROLL NUMBER", font=(cs.font_2, 15, "bold"), bg=cs.color_1).place(x=130,y=100)
        sturoll = Label(self.frame_1, text=row[2], font=(cs.font_1, 10))
        sturoll.place(x=130,y=130, width=200)

        student_name = Label(self.frame_1, text="STUDENT NAME", font=(cs.font_2, 15, "bold"), bg=cs.color_1).place(x=400,y=100)
        stuname = Label(self.frame_1, text=row[3], font=(cs.font_1, 10))
        stuname.place(x=400,y=130, width=200)

        course = Label(self.frame_1, text="COURSE", font=(cs.font_2, 15, "bold"), bg=cs.color_1).place(x=130,y=170)
        Course = Label(self.frame_1, text=row[4], font=(cs.font_1, 10))
        Course.place(x=130,y=200, width=200)

        subject = Label(self.frame_1, text="SUBJECT", font=(cs.font_2, 15, "bold"), bg=cs.color_1).place(x=400,y=170)
        Subject = Label(self.frame_1, text=row[5], font=(cs.font_1, 10))
        Subject.place(x=400,y=200, width=200)

        issue_date = Label(self.frame_1, text="ISSUE DATE", font=(cs.font_2, 15, "bold"), bg=cs.color_1).place(x=130,y=240)
        issuedate = Label(self.frame_1, text=row[6], font=(cs.font_1, 10))
        issuedate.place(x=130,y=270, width=200)

        return_date = Label(self.frame_1, text="RETURN DATE", font=(cs.font_2, 15, "bold"), bg=cs.color_1).place(x=400,y=240)
        self.return_date_entry = Entry(self.frame_1, bg=cs.color_4, fg=cs.color_3)
        self.return_date_entry.insert(0, row[7])
        self.return_date_entry.place(x=400,y=270, width=200)

        self.submit_bt = Button(self.frame_1, text='SUBMIT', font=(cs.font_1, 12), bd=2, command=partial(self.BorrowBookAgain, row),cursor="hand2", bg=cs.color_2,fg=cs.color_3).place(x=300,y=320,width=100)
    
    # Function 7: It gets call 'Function 6', modify the return date in the 'borrow_record'
    # table.
    def BorrowBookAgain(self, row):
        try:
            connection = pymysql.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
            curs = connection.cursor()
            curs.execute("update borrow_record set return_date=%s where stu_roll=%s and book_id=%s",
            (
                self.return_date_entry.get(),
                row[2],
                row[0]
            ))
            messagebox.showinfo("SUCCESS!", "THE BOOK IS ISSUED AGAIN")
            connection.commit()
            connection.close()
            self.ClearScreen()
        except Exception as e:
            messagebox.showerror("Error!",f"Error due to {str(e)}",parent=self.window)

    # Function 8: It takes the roll no of a student to see the book 
    # details borrowed by that student
    def ReturnBook(self):
        self.ClearScreen()
        return_book = Label(self.frame_1, text="RETURN BOOK", font=(cs.font_1, 30, "bold"), bg=cs.color_4).place(x=250, y=40)
        roll_no = Label(self.frame_1, text="ENTER THE ROOL NUMBER.", font=(cs.font_2, 15, "bold"), bg=cs.color_1).place(x=210,y=140)
        self.roll_no_entry = Entry(self.frame_1, bg=cs.color_4, fg=cs.color_3)
        self.roll_no_entry.place(x=210,y=175, width=300)
        
        self.search_bt = Button(self.frame_1, text='SEARCH', font=(cs.font_1, 12), bd=2, command=self.ShowRecordsforReturn,cursor="hand2", bg=cs.color_2,fg=cs.color_3).place(x=310,y=215,width=100)

    # Function 9: It gets call from 'Function 3', is used to update 
    # a book record(book name, author, edition, price, quantity, etc.)
    def UpdateBookDetails(self):
        x = self.tree.selection()
        row = self.tree.item(x)['values']

        self.ClearScreen()

        book_id = Label(self.frame_1, text="BOOK ID", font=(cs.font_2, 18, "bold"), bg=cs.color_1).place(x=220,y=30)
        id = Label(self.frame_1, text=row[0], font=(cs.font_1, 10))
        id.place(x=220,y=60, width=300)

        book_name = Label(self.frame_1, text="BOOK NAME", font=(cs.font_2, 15, "bold"), bg=cs.color_1).place(x=220,y=100)
        self.bookname_entry = Entry(self.frame_1, bg=cs.color_4, fg=cs.color_3)
        self.bookname_entry.insert(0, row[1])
        self.bookname_entry.place(x=220,y=130, width=300)

        author = Label(self.frame_1, text="AUTHOR", font=(cs.font_2, 15, "bold"), bg=cs.color_1).place(x=220,y=170)
        self.author_entry = Entry(self.frame_1, bg=cs.color_4, fg=cs.color_3)
        self.author_entry.insert(0, row[2])
        self.author_entry.place(x=220,y=200, width=300)

        edition = Label(self.frame_1, text="EDITION", font=(cs.font_2, 15, "bold"), bg=cs.color_1).place(x=220,y=240)
        self.edition_entry = Entry(self.frame_1, bg=cs.color_4, fg=cs.color_3)
        self.edition_entry.insert(0, row[3])
        self.edition_entry.place(x=220,y=270, width=300)

        price = Label(self.frame_1, text="PRICE", font=(cs.font_2, 15, "bold"), bg=cs.color_1).place(x=220,y=310)
        self.price_entry = Entry(self.frame_1, bg=cs.color_4, fg=cs.color_3)
        self.price_entry.insert(0, row[4])
        self.price_entry.place(x=220,y=340, width=300)

        quantity = Label(self.frame_1, text="QUANTITY", font=(cs.font_2, 15, "bold"), bg=cs.color_1).place(x=220,y=380)
        self.qty_entry = Entry(self.frame_1, bg=cs.color_4, fg=cs.color_3)
        self.qty_entry.insert(0, row[5])
        self.qty_entry.place(x=220,y=410, width=300)

        self.submit_bt_1 = Button(self.frame_1, text='SUBMIT', font=(cs.font_1, 12), bd=2, command=partial(self.SubmitforUpdateBook, row), cursor="hand2", bg=cs.color_2,fg=cs.color_3).place(x=310,y=459,width=100)

    # Function 10: It gets call from 'Function 9' when the submit button is pressed.
    # It updates a entry in the 'book_list' table
    def SubmitforUpdateBook(self, row):
        try:
            connection = pymysql.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
            curs = connection.cursor()
            curs.execute("update book_list set book_name=%s,author=%s,edition=%s,price=%s,qty=%s where book_id=%s",
            (
                self.bookname_entry.get(),
                self.author_entry.get(),
                self.edition_entry.get(),
                self.price_entry.get(),
                self.qty_entry.get(),
                row[0]
            ))
            messagebox.showinfo("SUCCESS!", "THE DATA HAS BEEN UPDATED")
            connection.commit()
            connection.close()
            self.ClearScreen()
        except Exception as e:
            messagebox.showerror("Error!",f"Error due to {str(e)}",parent=self.window)

    # Function 11: It takes the data from the user to issue a book for the students
    # and calls 'Function 22' when the submit button is pressed
    def GetData_for_IssueBook(self):
        self.ClearScreen()

        book_id = Label(self.frame_1, text="BOOK ID", font=(cs.font_2, 15, "bold"), bg=cs.color_1).place(x=130,y=30)
        self.book_id_entry = Entry(self.frame_1, bg=cs.color_4, fg=cs.color_3)
        self.book_id_entry.place(x=130,y=60, width=200)

        book_name = Label(self.frame_1, text="BOOK NAME", font=(cs.font_2, 15, "bold"), bg=cs.color_1).place(x=400,y=30)
        self.book_name_entry = Entry(self.frame_1, bg=cs.color_4, fg=cs.color_3)
        self.book_name_entry.place(x=400,y=60, width=200)

        student_roll = Label(self.frame_1, text="STUDENT ROLL NUMBER", font=(cs.font_2, 15, "bold"), bg=cs.color_1).place(x=130,y=100)
        self.stu_roll_entry = Entry(self.frame_1, bg=cs.color_4, fg=cs.color_3)
        self.stu_roll_entry.place(x=130,y=130, width=200)

        student_name = Label(self.frame_1, text="STUDENT NAME", font=(cs.font_2, 15, "bold"), bg=cs.color_1).place(x=400,y=100)
        self.stu_name_entry = Entry(self.frame_1, bg=cs.color_4, fg=cs.color_3)
        self.stu_name_entry.place(x=400,y=130, width=200)

        course = Label(self.frame_1, text="COURSE", font=(cs.font_2, 15, "bold"), bg=cs.color_1).place(x=130,y=170)
        self.course_entry = Entry(self.frame_1, bg=cs.color_4, fg=cs.color_3)
        self.course_entry.place(x=130,y=200, width=200)

        subject = Label(self.frame_1, text="SUBJECT", font=(cs.font_2, 15, "bold"), bg=cs.color_1).place(x=400,y=170)
        self.subject_entry = Entry(self.frame_1, bg=cs.color_4, fg=cs.color_3)
        self.subject_entry.place(x=400,y=200, width=200)

        issue_date = Label(self.frame_1, text="ISSUE DATE", font=(cs.font_2, 15, "bold"), bg=cs.color_1).place(x=130,y=240)
        self.issue_date_entry = Entry(self.frame_1, bg=cs.color_4, fg=cs.color_3)
        self.issue_date_entry.place(x=130,y=270, width=200)

        return_date = Label(self.frame_1, text="RETURN DATE", font=(cs.font_2, 15, "bold"), bg=cs.color_1).place(x=400,y=240)
        self.return_date_entry = Entry(self.frame_1, bg=cs.color_4, fg=cs.color_3)
        self.return_date_entry.place(x=400,y=270, width=200)

        self.submit_bt_1 = Button(self.frame_1, text='SUBMIT', font=(cs.font_1, 12), bd=2, command=self.Submit_borrow_data,cursor="hand2", bg=cs.color_2,fg=cs.color_3).place(x=300,y=320,width=100)
    
    # Function 12: It is used get the book name for searching and calls 'Function 17'
    # when the search button is pressed
    def GetBookNametoSearch(self):
        self.ClearScreen()
        search_book = Label(self.frame_1, text="SEARCH BOOK", font=(cs.font_1, 30, "bold"), bg=cs.color_4).place(x=250, y=40)
        book_name = Label(self.frame_1, text="ENTER THE BOOK NAME", font=(cs.font_2, 15, "bold"), bg=cs.color_1).place(x=220,y=140)
        self.book_entry = Entry(self.frame_1, bg=cs.color_4, fg=cs.color_3)
        self.book_entry.place(x=220,y=175, width=300)
        
        self.search_bt = Button(self.frame_1, text='SEARCH', font=(cs.font_1, 12), bd=2, command=self.SearchBook,cursor="hand2", bg=cs.color_2,fg=cs.color_3).place(x=310,y=215,width=100)

    # Function 13: It takes the student roll number and calls 'Function 15' for
    # performing return book operation (when the search button is pressed)
    def ReturnBook(self):
        self.ClearScreen()
        return_book = Label(self.frame_1, text="RETURN BOOK", font=(cs.font_1, 30, "bold"), bg=cs.color_4).place(x=250, y=40)
        roll_no = Label(self.frame_1, text="ENTER THE ROLL NUMBER", font=(cs.font_2, 15, "bold"), bg=cs.color_1).place(x=210,y=140)
        self.roll_no_entry = Entry(self.frame_1, bg=cs.color_4, fg=cs.color_3)
        self.roll_no_entry.place(x=210,y=175, width=300)
        
        self.search_bt = Button(self.frame_1, text='SEARCH', font=(cs.font_1, 12), bd=2, command=self.ShowRecordsforReturn,cursor="hand2", bg=cs.color_2,fg=cs.color_3).place(x=310,y=215,width=100)

    # Function 14:
    def ShowBooks(self):
        self.ClearScreen()
        # Defining two scrollbars
        scroll_x = ttk.Scrollbar(self.frame_1, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(self.frame_1, orient=VERTICAL)
        self.tree = ttk.Treeview(self.frame_1, columns=cs.columns, height=400, selectmode="extended", yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        scroll_y.config(command=self.tree.yview)
        # vertical scrollbar: left side
        scroll_y.pack(side=LEFT, fill=Y)
        scroll_x.config(command=self.tree.xview)
        # Horizontal scrollbar: at bottom
        scroll_x.pack(side=BOTTOM, fill=X)

        # Table headings
        self.tree.heading('book_id', text='BOOK ID', anchor=W)
        self.tree.heading('book_name', text='BOOK NAME', anchor=W)
        self.tree.heading('author', text='AUTHOR', anchor=W)
        self.tree.heading('edition', text='EDITION', anchor=W)
        self.tree.heading('price', text='PRICE', anchor=W)
        self.tree.heading('qty', text='QUANTITY', anchor=W)
        self.tree.pack()
        # Double click on a row
        self.tree.bind('<Double-Button-1>', self.OnSelectedforShowBooks)

        try:
            connection = pymysql.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
            curs = connection.cursor()
            curs.execute("select * from book_list")
            rows=curs.fetchall()

            if rows == None:
                messagebox.showinfo("DATABASE EMPTY!","THERE IS NO DATABASE TO SHOW",parent=self.window)
                connection.close()
                self.ClearScreen()
            else:
                connection.close()
        except Exception as e:
            messagebox.showerror("Error!",f"Error due to {str(e)}",parent=self.window)

        for list in rows:
            self.tree.insert("", 'end', text=(rows.index(list)+1), values=(list[0], list[1], list[2], list[3], list[4], list[5]))

    # Function 15: It gets call from 'Function 13' and shows all the book records
    # taken by a student as per the roll number. If the users select a record, they
    # can delete that record or issue the book again for the student
    def ShowRecordsforReturn(self):
        if self.roll_no_entry.get() == "":
            messagebox.showerror("ERROR!", "PLEASE ENTER THE ROLL NUMBER")
        else:
            try:
                connection = pymysql.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
                curs = connection.cursor()
                curs.execute("select * from borrow_record where stu_roll=%s", self.roll_no_entry.get())
                rows=curs.fetchall()
                
                if len(rows) == 0:
                    messagebox.showerror("ERROR!","THIS ROLL NUMBER DOESN'T EXISTS",parent=self.window)
                    connection.close()
                    self.roll_no_entry.delete(0, END)
                else:
                    connection.close()
                    self.ClearScreen()

                    # Defining two scrollbars
                    scroll_x = ttk.Scrollbar(self.frame_1, orient=HORIZONTAL)
                    scroll_y = ttk.Scrollbar(self.frame_1, orient=VERTICAL)
                    self.tree_1 = ttk.Treeview(self.frame_1, columns=cs.columns_1, height=400, selectmode="extended", yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
                    scroll_y.config(command=self.tree_1.yview)
                    # vertical scrollbar: left side
                    scroll_y.pack(side=LEFT, fill=Y)
                    scroll_x.config(command=self.tree_1.xview)
                    # Horizontal scrollbar: at bottom
                    scroll_x.pack(side=BOTTOM, fill=X)

                    # Table headings
                    self.tree_1.heading('book_id', text='BOOK ID', anchor=W)
                    self.tree_1.heading('book_name', text='BOOK NAME', anchor=W)
                    self.tree_1.heading('student_roll', text='STUDENT ROLL NUMBER', anchor=W)
                    self.tree_1.heading('student_name', text='STUDENT NAME', anchor=W)
                    self.tree_1.heading('course', text='COURSE', anchor=W)
                    self.tree_1.heading('subject', text='SUBJECT', anchor=W)
                    self.tree_1.heading('issue_date', text='ISSUE DATE', anchor=W)
                    self.tree_1.heading('return_date', text='RETURN DATE', anchor=W)

                    self.tree_1.pack()
                    # Double click on a row
                    self.tree_1.bind('<Double-Button-1>', self.OnSelectedforReturn)

                    for list in rows:
                        self.tree_1.insert("", 'end', text=(rows.index(list)+1), values=(list[0], list[1], list[2], list[3], list[4], list[5], list[6], list[7]))
            except Exception as e:
                messagebox.showerror("Error!",f"Error due to {str(e)}",parent=self.window)

    # Function 16: It gets call when the user pressed 'Book Holders' button and shows 
    # all the book records taken by a student. If the users select a record, they
    # can delete that record or issue the book again for the student. 
    def AllBorrowRecords(self):
        self.ClearScreen()
        # Defining two scrollbars
        scroll_x = ttk.Scrollbar(self.frame_1, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(self.frame_1, orient=VERTICAL)
        self.tree_1 = ttk.Treeview(self.frame_1, columns=cs.columns_1, height=400, selectmode="extended", yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        scroll_y.config(command=self.tree_1.yview)
        # vertical scrollbar: left side
        scroll_y.pack(side=LEFT, fill=Y)
        scroll_x.config(command=self.tree_1.xview)
        # Horizontal scrollbar: at bottom
        scroll_x.pack(side=BOTTOM, fill=X)

        # Table headings
        self.tree_1.heading('book_id', text='BOOK ID', anchor=W)
        self.tree_1.heading('book_name', text='BOOK NAME', anchor=W)
        self.tree_1.heading('student_roll', text='STUDENT ROLL NUMBER', anchor=W)
        self.tree_1.heading('student_name', text='STUDENT NAME', anchor=W)
        self.tree_1.heading('course', text='COURSE', anchor=W)
        self.tree_1.heading('subject', text='SUBJECT', anchor=W)
        self.tree_1.heading('issue_date', text='ISSUE DATE', anchor=W)
        self.tree_1.heading('return_date', text='RETURN DATE', anchor=W)

        self.tree_1.pack()
        # Double click on a row
        self.tree_1.bind('<Double-Button-1>', self.OnSelectedforBorrowRecords)

        try:
            connection = pymysql.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
            curs = connection.cursor()
            curs.execute("select * from borrow_record")
            rows=curs.fetchall()

            if rows == None:
                messagebox.showinfo("Database Empty","There is no data to show",parent=self.window)
                connection.close()
                self.ClearScreen()
            else:
                connection.close()
        except Exception as e:
            messagebox.showerror("Error!",f"Error due to {str(e)}",parent=self.window)

        for list in rows:
            self.tree_1.insert("", 'end', text=(rows.index(list)+1), values=(list[0], list[1], list[2], list[3], list[4], list[5], list[6], list[7]))
    
    # Function 17: It gets call from 'Function 12' and search a book by the name
    def SearchBook(self):
        if self.book_entry.get() == "":
            messagebox.showerror("Error!", "Please Enter the Book Name")
        else:
            try:
                connection = pymysql.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
                curs = connection.cursor()
                curs.execute("select * from book_list where book_name like %s", ("%" + self.book_entry.get() + "%"))
                rows=curs.fetchall()
                if rows == None:
                    messagebox.showinfo("Database Empty","There is no data to show",parent=self.window)
                    connection.close()
                    self.ClearScreen()
                else:
                    connection.close()
            except Exception as e:
                messagebox.showerror("Error!",f"Error due to {str(e)}",parent=self.window)
                
            # Defining two scrollbars
            scroll_x = ttk.Scrollbar(self.frame_1, orient=HORIZONTAL)
            scroll_y = ttk.Scrollbar(self.frame_1, orient=VERTICAL)
            self.tree = ttk.Treeview(self.frame_1, columns=cs.columns, height=400, selectmode="extended", yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
            scroll_y.config(command=self.tree.yview)
            # vertical scrollbar: left side
            scroll_y.pack(side=LEFT, fill=Y)
            scroll_x.config(command=self.tree.xview)
            # Horizontal scrollbar: at bottom
            scroll_x.pack(side=BOTTOM, fill=X)

            # Table headings
            self.tree.heading('book_id', text='BOOK ID', anchor=W)
            self.tree.heading('book_name', text='BOOK NAME', anchor=W)
            self.tree.heading('author', text='AUTHOR', anchor=W)
            self.tree.heading('edition', text='EDITION', anchor=W)
            self.tree.heading('price', text='PRICE', anchor=W)
            self.tree.heading('qty', text='QUANTITY', anchor=W)
            self.tree.pack()
            # Double click on a row
            self.tree.bind('<Double-Button-1>', self.OnSelectedforShowBooks)

            for list in rows:
                self.tree.insert("", 'end', text=(rows.index(list)+1), values=(list[0], list[1], list[2], list[3], list[4], list[5]))
    
    # # Function 18: No longer required
    # def UpdateBook(self):
    #     x = self.tree.selection()
    #     y=self.tree.item(x)['values']
    #     if y=="":
    #         messagebox.showerror('Error!', "Please select a record")
    #     else:
    #         try:
    #             connection = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
    #             curs = connection.cursor()
    #             curs.execute("select * from book_list where book_id=%s", y[0])
    #             row=curs.fetchone()
    #             # self.GetData_to_Update(row)
    #             connection.close()
    #         except Exception as e:
    #             messagebox.showerror("Error!",f"Error due to {str(e)}",parent=self.window)
    


    # Function 19: This function displays widgets for adding new books
    def AddNewBook(self):
        self.ClearScreen()

        book_id = Label(self.frame_1, text="BOOK ID", font=(cs.font_2, 15, "bold"), bg=cs.color_1).place(x=220,y=30)
        self.id_entry = Entry(self.frame_1, bg=cs.color_4, fg=cs.color_3)
        self.id_entry.place(x=220,y=60, width=300)

        book_name = Label(self.frame_1, text="BOOK NAME", font=(cs.font_2, 15, "bold"), bg=cs.color_1).place(x=220,y=100)
        self.bookname_entry = Entry(self.frame_1, bg=cs.color_4, fg=cs.color_3)
        self.bookname_entry.place(x=220,y=130, width=300)

        author = Label(self.frame_1, text="AUTHOR", font=(cs.font_2, 15, "bold"), bg=cs.color_1).place(x=220,y=170)
        self.author_entry = Entry(self.frame_1, bg=cs.color_4, fg=cs.color_3)
        self.author_entry.place(x=220,y=200, width=300)

        edition = Label(self.frame_1, text="EDITION", font=(cs.font_2, 15, "bold"), bg=cs.color_1).place(x=220,y=240)
        self.edition_entry = Entry(self.frame_1, bg=cs.color_4, fg=cs.color_3)
        self.edition_entry.place(x=220,y=270, width=300)

        price = Label(self.frame_1, text="PRICE", font=(cs.font_2, 15, "bold"), bg=cs.color_1).place(x=220,y=310)
        self.price_entry = Entry(self.frame_1, bg=cs.color_4, fg=cs.color_3)
        self.price_entry.place(x=220,y=340, width=300)

        quantity = Label(self.frame_1, text="QUANTITY", font=(cs.font_2, 15, "bold"), bg=cs.color_1).place(x=220,y=380)
        self.qty_entry = Entry(self.frame_1, bg=cs.color_4, fg=cs.color_3)
        self.qty_entry.place(x=220,y=410, width=300)

        self.submit_bt_1 = Button(self.frame_1, text='SUBMIT', font=(cs.font_1, 12), bd=2, command=self.Submit,cursor="hand2", bg=cs.color_2,fg=cs.color_3).place(x=310,y=459,width=100)

    # # Function 20: No longer required
    # def GetDataforUpdate(self):
    #     self.ClearScreen()

    #     book_id = Label(self.frame_1, text="Book Id", font=(cs.font_2, 15, "bold"), bg=cs.color_1).place(x=220,y=30)
    #     self.id_entry = Entry(self.frame_1, bg=cs.color_4, fg=cs.color_3)
    #     self.id_entry.place(x=220,y=60, width=300)

    #     book_name = Label(self.frame_1, text="Book Name", font=(cs.font_2, 15, "bold"), bg=cs.color_1).place(x=220,y=100)
    #     self.bookname_entry = Entry(self.frame_1, bg=cs.color_4, fg=cs.color_3)
    #     self.bookname_entry.place(x=220,y=130, width=300)

    #     author = Label(self.frame_1, text="Author", font=(cs.font_2, 15, "bold"), bg=cs.color_1).place(x=220,y=170)
    #     self.author_entry = Entry(self.frame_1, bg=cs.color_4, fg=cs.color_3)
    #     self.author_entry.place(x=220,y=200, width=300)

    #     edition = Label(self.frame_1, text="Edition", font=(cs.font_2, 15, "bold"), bg=cs.color_1).place(x=220,y=240)
    #     self.edition_entry = Entry(self.frame_1, bg=cs.color_4, fg=cs.color_3)
    #     self.edition_entry.place(x=220,y=270, width=300)

    #     price = Label(self.frame_1, text="Price", font=(cs.font_2, 15, "bold"), bg=cs.color_1).place(x=220,y=310)
    #     self.price_entry = Entry(self.frame_1, bg=cs.color_4, fg=cs.color_3)
    #     self.price_entry.place(x=220,y=340, width=300)

    #     quantity = Label(self.frame_1, text="Quantity", font=(cs.font_2, 15, "bold"), bg=cs.color_1).place(x=220,y=380)
    #     self.qty_entry = Entry(self.frame_1, bg=cs.color_4, fg=cs.color_3)
    #     self.qty_entry.place(x=220,y=410, width=300)
    #     self.submit_bt_1 = Button(self.frame_1, text='Submit', font=(cs.font_1, 12), bd=2, command=self.Submit,cursor="hand2", bg=cs.color_2,fg=cs.color_3).place(x=310,y=459,width=100)



    # Function 21: This function adds a new book record'''
    def Submit(self):
        if self.id_entry.get() == "" or self.bookname_entry.get() == "" or self.author_entry.get() == "" or self.edition_entry.get() == "" or self.price_entry.get() == "" or self.qty_entry.get() == "":
            messagebox.showerror("Error!","Sorry!, All fields are required",parent=self.window)
        else:
            try:
                connection = pymysql.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
                curs = connection.cursor()
                curs.execute("select * from book_list where book_id=%s", self.id_entry.get())
                row=curs.fetchone()

                if row!=None:
                    messagebox.showerror("Error!","This book id is already exists, please try again with another one",parent=self.window)
                else:
                    curs.execute("insert into book_list (book_id,book_name,author,edition,price,qty) values(%s,%s,%s,%s,%s,%s)",
                                        (
                                            self.id_entry.get(),
                                            self.bookname_entry.get(),
                                            self.author_entry.get(),
                                            self.edition_entry.get(),
                                            self.price_entry.get(),
                                            self.qty_entry.get()  
                                        ))
                    connection.commit()
                    connection.close()
                    messagebox.showinfo('Done!', "The data has been submitted")
                    self.reset_fields()
            except Exception as e:
                messagebox.showerror("Error!",f"Error due to {str(e)}",parent=self.window)

    # Function 22: This function gets call from 'Function 11', is used to submit
    # data to issue a book
    def Submit_borrow_data(self):
        if self.book_id_entry.get()=="" or self.book_name_entry.get()=="" or self.stu_roll_entry.get()=="" or self.stu_name_entry.get()=="" or self.issue_date_entry.get()=="" or self.return_date_entry.get=="" or self.course_entry.get()=="" or self.subject_entry.get()=="":
            messagebox.showerror("Error!","Sorry!, All fields are required",parent=self.window)
        else:
            try:
                connection = pymysql.connect(host=cr.host, user=cr.user, password=cr.password, database=cr.database)
                curs = connection.cursor()
                curs.execute("select * from book_list where book_id=%s", self.book_id_entry.get())
                row=curs.fetchone()
                book_quantity = row[5]
                if row==None:
                    messagebox.showerror("Error!","This book isn't exist",parent=self.window)
                elif book_quantity == 1:
                    messagebox.showwarning("Notification", "This copy is left only one, you can't take it")
                else:
                    curs.execute("select * from borrow_record where stu_roll=%s and book_id=%s", (self.stu_roll_entry.get(),self.book_id_entry.get()))
                    row=curs.fetchone()
                    if row != None:
                        messagebox.showerror("Error!", "This book is already taken by the student")
                        connection.close()
                    else:
                        curs.execute("select * from borrow_record where stu_roll=%s", self.stu_roll_entry.get())
                        rows = curs.fetchall()
                        if len(rows) >= 3:
                            messagebox.showerror("Max. 3 books to each student", "Borrow books limit has exceed")
                            connection.close()
                        else:
                            curs.execute("insert into borrow_record (book_id,book_name,stu_roll,stu_name,course,subject,issue_date,return_date) values(%s,%s,%s,%s,%s,%s,%s,%s)",
                                                (
                                                    self.book_id_entry.get(),
                                                    self.book_name_entry.get(),
                                                    self.stu_roll_entry.get(),
                                                    self.stu_name_entry.get(),
                                                    self.course_entry.get(),
                                                    self.subject_entry.get(),
                                                    self.issue_date_entry.get(),
                                                    self.return_date_entry.get()
                                                ))
                            book_quantity -= 1
                            curs.execute("update book_list set qty=%s where book_id=%s", (book_quantity,self.book_id_entry.get()))
                            connection.commit()
                            connection.close()
                            messagebox.showinfo('Done!', "The data has been submitted")
                            self.reset_issuebook_fields()
            except Exception as e:
                messagebox.showerror("Error!",f"Error due to {str(e)}",parent=self.window)
    
    # Reset all the entry fields of add new book form
    def reset_fields(self):
        self.id_entry.delete(0, END)
        self.bookname_entry.delete(0, END)
        self.author_entry.delete(0, END)
        self.edition_entry.delete(0, END)
        self.price_entry.delete(0, END)
        self.qty_entry.delete(0, END)
    
    # Reset all the entry fields issue a book form
    def reset_issuebook_fields(self):
        self.book_id_entry.delete(0, END)
        self.book_name_entry.delete(0, END)
        self.stu_roll_entry.delete(0, END)
        self.stu_name_entry.delete(0, END)
        self.course_entry.delete(0, END)
        self.subject_entry.delete(0, END)
        self.issue_date_entry.delete(0, END)
        self.return_date_entry.delete(0, END)

    # Removes all widgets from the frame 1 and frame 3
    def ClearScreen(self):
        for widget in self.frame_1.winfo_children():
            widget.destroy()

        for widget in self.frame_3.winfo_children():
            widget.destroy()

    '''Exit window'''
    def Exit(self):
        self.window.destroy()

# The main function
if __name__ == "__main__":
    root = Tk()
    obj = Management(root)
    root.mainloop()

# Kivy-login-screen
#making kivy login screen with mobile phone

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty,NumericProperty
import smtplib
import random
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.clock import Clock
from kivy.uix.progressbar import ProgressBar
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.core.window import Window
import sqlite3
import random
from email.message import EmailMessage
from kivy.uix.popup import Popup

#loading the kivy file
Builder.load_file('login.kv')
# defining global variables 
global_email=''
global_generated_otp=''
generated_otp=''

 

class welcome_screen(Screen):
    def on_enter(self):
        Clock.schedule_interval(self.load_screen,0.1)
       
    def load_screen(self,dt):
        if self.ids.progressbar.value < self.ids.progressbar.max:
            self.ids.progressbar.value +=2
            self.ids.status.text='...Loading,please wait'
            
            if self.ids.progressbar.value == self.ids.progressbar.max:
                self.manager.current='signup_screen'
        
        
        
        
        
    
   

    
    
class signup_screen(Screen):
    def signup(self,name,email,password1,password2):
        #create table in sqlite      
        conn=sqlite3.connect('login.db',timeout=10)
        cursor=conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS login_system(name TEXT,email TEXT NULL UNIQUE,password TEXT NULL)''')
        conn.commit()
        
     

        
        if not name or not email or not  password1 or not password2:
            self.ids.status.text='All fields are required'
        elif password1 != password2:
            self.ids.status.text='Password mismatched'
        else:
           try:
               cursor.execute('SELECT email FROM login_system WHERE email =? ',(email,))
               results=cursor.fetchone()
               if results:
                    self.ids.status.text='User already exists'
                    conn.commit()
                    conn.close()
               else:
                    try:
                        popup=Popup(title='Success',content =Label(text='Registered successfull'),size_hint=(0.4,0.3))
                        popup.open()
                        Clock.schedule_interval(lambda dt:popup.dismiss(),1)
                         
                        conn=sqlite3.connect('login.db',timeout=10)
                        cursor=conn.cursor() 
                        cursor.execute('INSERT INTO login_system(name,password,email) VALUES (?,?,?)',(name,password1,email))
                        conn.commit()
                        conn.close()
                        self.manager.current='login_screen'
                        
                       
                    except  sqlite3.Error as e:
                        self.ids.status.text=f'{e}'  
                        conn.close()
                    except  Exception as e:
                        self.ids.status.text=f'{e}'
                        
           except  sqlite3.Error as e:
                    self.ids.status.text=f'{e}'  
                    conn.close()
           except  Exception as e:
                    self.ids.status.text=f'{e}'
           
              
           
               
                
            
            
            
                
                
            

            
            
class login_screen(Screen):
    def check_details(self,password):
       global global_generated_otp,global_email
       
       global_email=self.ids.email.text.strip()
       
       
       
       conn=sqlite3.connect('login.db',timeout=5)
       cursor=conn.cursor()
       
       
       if not global_email or not password:
            self.ids.status.text='All fields are required'
       else:   
                        
        
                            
        
                            #generate otp
                            generated_otp=str(random.randint(1000,100000))
                            global_generated_otp=generated_otp
                            
                            
                                
                                
                            try:
                                cursor.execute('SELECT * FROM login_system WHERE email =? AND password = ? ',(global_email,password))
                                results=cursor.fetchall()
                                if results :
                                        popup=Popup(title='Otp verification sent',content =Label(text='Check your email \n for otp verification'),size_hint=(0.4,0.3))
                                    
                                        
                                        popup.open()
                                        Clock.schedule_interval(lambda dt:popup.dismiss(),7)
                                        
                                        
                                
                                #send otp to email
                                        em=EmailMessage()
                                        receiver=f'{global_email}'
                                        sender='Pemwatechnologies@gmail.com'
                                        subject='Otp verification'
                                        body=f'your otp is :{generated_otp}'
                                        app_password='(your google app password)' 
                                    
                                    
                                        em['To']=receiver
                                        em['From']=sender
                                        em['Subject']=subject
                                        em.set_content(body)
                                       
                                        server=smtplib.SMTP('smtp.gmail.com',587)
                                        server.starttls()
                                        server.login(sender,app_password)
                                        server.send_message(em)
                                        server.close()
                                        
                                        Clock.schedule_interval(lambda dt:popup.dismiss(),5)
                                        conn.commit()

                                        conn.close()
                                        self.manager.current='otp_screen'
                                        
                                        
                                                      
                                        
                                else:
                                        self.ids.status.text='invalid credentials   \n   sign up'
                                    
                                
                                   
                                   
                                    
                            except Exception as e: 
                                self.ids.status.text=f'{e}'
                            
                                
                            except Exception as e:   
                                self.ids.status.text=f'{e}'
                            
                          

                

    
class otp_screen(Screen):
   
    
    def resend_otp(self):
             global global_email,generated_otp
             
             generated_otp=str(random.randint(1000,100000))
             
             
             popup=Popup(title='Otp verification sent',content =Label(text='otp was sent to your email'),size_hint=(0.4,0.3))
             popup.open()
             Clock.schedule_interval(lambda dt:popup.dismiss(),7)
             
             #send otp to email
             em=EmailMessage()
             receiver=f'{global_email}'
             sender='Pemwatechnologies@gmail.com'
             subject='Otp verification'
             body=f'your otp is :{generated_otp}'
             app_password='(your google app password)'
             em['To']=receiver
             em['From']=sender
             em['Subject']=subject
             em.set_content(body)
             server=smtplib.SMTP('smtp.gmail.com',587)
             server.starttls()
             server.login(sender,app_password)
             server.send_message(em)
             server.close()
             self.manager.current='resend_otp_screen'
             
             
                                
             
    def check_otp(self):
       global global_generated_otp
       otp_input=self.ids.otp.text
       
     

        
       if not otp_input:
            self.ids.status.text='Enter otp for verification'
        
            
        
       elif  otp_input != global_generated_otp:
           self.ids.status.text=f'Invalid otp'
           
           
       
       
       
           
       else:
           popup=Popup(title='Success',content =Label(text='otp verification successfull'),size_hint=(0.6,0.2))
           popup.open()
           Clock.schedule_interval(lambda dt:popup.dismiss(),1)
           
           
           self.manager.current='dashboard_screen'
        

            
            
                
            
class resend_otp_screen(Screen):
   
    
    def resend_otp(self):
             global global_email,generated_otp
             
             generated_otp=str(random.randint(1000,100000))
             
             
             popup=Popup(title='Otp verification sent',content =Label(text='Check your email \n for otp verification'),size_hint=(0.4,0.3))
             popup.open()
             Clock.schedule_interval(lambda dt:popup.dismiss(),7)
             
             #send otp to email
             em=EmailMessage()
             receiver=f'{global_email}'
             sender='Pemwatechnologies@gmail.com'
             subject='Otp verification'
             body=f'your otp is :{generated_otp}'
             app_password='(your google app password)'
             em['To']=receiver
             em['From']=sender
             em['Subject']=subject
             em.set_content(body)
             server=smtplib.SMTP('smtp.gmail.com',587)
             server.starttls()
             server.login(sender,app_password)
             server.send_message(em)
             server.close()
            
             
             
                                
             
    def check_otp(self):
       global generated_otp
       otp_input=self.ids.otp.text
       
     

        
       if not otp_input:
            self.ids.status.text='Enter otp for verification'
        
            
        
       elif  otp_input != generated_otp:
           self.ids.status.text=f'Invalid otp'
          
       
       
       
           
       else:
           popup=Popup(title='Success',content =Label(text='otp verification successfull'),size_hint=(0.6,0.2))
           popup.open()
           Clock.schedule_interval(lambda dt:popup.dismiss(),1)
           
           
           self.manager.current='dashboard_screen'
                    
    
    
class dashboard_screen(Screen):
    pass    
    
class app(App):
    def build(self):
        otp=''
        email=''
        
        sm=ScreenManager()
       
        sm.add_widget(welcome_screen(name='welcome_screen'))
        sm.add_widget(login_screen(name='login_screen'))
        sm.add_widget(signup_screen(name='signup_screen'))
        sm.add_widget(otp_screen(name='otp_screen'))
        sm.add_widget(dashboard_screen(name='dashboard_screen'))
        sm.add_widget(resend_otp_screen(name='resend_otp_screen'))
        return sm
        
if __name__=='__main__':
        app().run()
        

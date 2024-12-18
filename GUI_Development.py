import tkinter as tk
from tkinter import *
import tkinter.messagebox
import customtkinter 
from PIL import Image, ImageTk
import pandas as pd
from tkinter import ttk
from pathlib import Path
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


# Set the OUTPUT_PATH and ASSETS_PATH directly
OUTPUT_PATH1 = Path(r".\figma\build 1\build")
ASSETS_PATH1 = OUTPUT_PATH1 / Path("assets/frame0")

OUTPUT_PATH2 = Path(r".\figma\build 2\build")
ASSETS_PATH2 = OUTPUT_PATH2 / Path("assets/frame0")

OUTPUT_PATH3 = Path(r".\figma\build 4\build")
ASSETS_PATH3 = OUTPUT_PATH3 / Path("assets/frame0")

def relative_to_assets1(path: str) -> Path:
    return ASSETS_PATH1 / Path(path)

def relative_to_assets2(path: str) -> Path:
    return ASSETS_PATH2 / Path(path)

def relative_to_assets3(path: str) -> Path:
    return ASSETS_PATH3 / Path(path)

customtkinter.set_appearance_mode("dark")  
customtkinter.set_default_color_theme("blue")

class ToplevelWindow_1(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('Display Dataset')
        self.geometry("1440x1024")
        self.configure(bg="#242424")


        self.canvas = Canvas(
            self,
            bg="#242424",
            height=1024,
            width=1440,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        self.image_image_1 = PhotoImage(file=relative_to_assets1("image_1.png"))
        self.image_1 = self.canvas.create_image(
            720.0,
            500.0,
            image=self.image_image_1
        )
        self.resizable(False, False)
        
        self.frame = customtkinter.CTkFrame(self, width=850, height=790)
        self.frame.place(relx=0.49, rely=0.56, anchor=CENTER)

        # Scrollbar vertikal
        self.scrollbar_y = ttk.Scrollbar(self, orient="vertical")
        self.scrollbar_y.place(x=1132, y=180, width=20, height=790)
        
        # Scrollbar horizontal
        self.scrollbar_x = ttk.Scrollbar(self, orient="horizontal")
        self.scrollbar_x.place(x=285, y=966, width=850, height=20)

        # Treeview untuk tabel
        self.tree = ttk.Treeview(
            self.frame, 
            yscrollcommand=self.scrollbar_y.set, 
            xscrollcommand=self.scrollbar_x.set
        )
        self.tree.place(relx=0, rely=0, width=850, height=790)

        # Sambungkan scrollbar ke Treeview
        self.scrollbar_y.config(command=self.tree.yview)
        self.scrollbar_x.config(command=self.tree.xview)

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('Treeview', background='#242424', fieldbackground='#242424', foreground='white')

    def display_dataset(self):
        # Load the dataset
        self.data = pd.read_csv('Fix_Cleaned_Dataset.csv', delimiter=',', engine='python')
        
        self.tree["columns"] = list(self.data.columns)
        self.tree["show"] = "headings"

        # Create columns in the Treeview
        for column in self.tree["columns"]:
            self.tree.heading(column, text=column, anchor=W)
            self.tree.column(column, stretch=NO, width=max(100, len(column) * 10))
        # Insert data into the Treeview
        for index, row in self.data.iterrows():
            self.tree.insert("", "end", values=list(row))

class ToplevelWindow_2(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('Dashboard Statistics')
        self.geometry("1260x1040")
        self.configure(bg="#242424")


        self.canvas = Canvas(
            self,
            bg="#242424",
            height=1040,
            width=1260,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)


        self.image_image_2 = PhotoImage(file=relative_to_assets2("image_1.png"))
        self.image_2 = self.canvas.create_image(
            630.0,
            520.0,
            image=self.image_image_2
        )
        self.resizable(False, False)

    def display_dataset2(self):
        self.data = pd.read_csv('Fix_Cleaned_Dataset.csv', delimiter=',', engine='python')
    
        city = self.data.loc[self.data[(self.data['Position'] == 'Data Analyst') & (self.data['Province'] == 'ON')].index, ['Province', 'City']].groupby('City').count()

        fig_1 = Figure(figsize=(5.62, 2.8), facecolor="#060B28")
        ax_1 = fig_1.add_subplot()
        ax_1.set_facecolor('#060B28')

        ax_1.barh(
            y=city.index,              
            width=city['Province'].values,  
            color="slateblue",          
            alpha=0.7                   
        )

        ax_1.plot(
            city['Province'].values,    
            city.index,                 
            color='violet',             
            linewidth=1.5,
            linestyle='--',              
            marker='o',                 
            markersize=4,               
            label="Peak"         
        )

        ax_1.tick_params(labelsize=5, colors='white')
        ax_1.grid(visible=True, color="gray", linestyle="--", alpha=0.5) 
        ax_1.set_xlabel("Count", fontsize=6, color="white")  
        ax_1.set_ylabel("City", fontsize=6, color="white")  
        ax_1.legend(loc="best", fontsize=6, facecolor="#060B28", edgecolor="violet", labelcolor="white")

        frame1 = FigureCanvasTkAgg(figure=fig_1, master=self)
        frame1.draw()
        frame1.get_tk_widget().place(x=230, y=395)


        # Fig 2
        fig_2 = Figure(figsize=(5.62, 2.8), facecolor="#060B28")
        ax_2 = fig_2.add_subplot()
        ax_2.set_facecolor('#060B28')

        sorted_counts = self.data['Position'].value_counts().sort_values(ascending=True)

        ax_2.barh(
            y=sorted_counts.index,              
            width=sorted_counts,  
            color="slateblue",         
            alpha=0.7                   
        )

        ax_2.tick_params(labelsize=5, colors='white')  
        ax_2.grid(visible=True, color="gray", linestyle="--", alpha=0.5)  
        ax_2.set_xlabel("Count", fontsize=6, color="white")  
        ax_2.set_ylabel("Job Role", fontsize=6, color="white")  
        
        frame2 = FigureCanvasTkAgg(figure=fig_2, master=self)
        frame2.draw()
        frame2.get_tk_widget().place(x=230, y=725)

        # Fig 3
        fig_3 = Figure(figsize=(4.10, 2.82), facecolor="#060B28")
        ax_3 = fig_3.add_subplot()
        ax_3.set_facecolor('#060B28')

        # Data untuk pie chart
        data_analyst_province = pd.Series({
            'ON': 151, 'BC': 36, 'AB': 35, 'QC': 32,
            'Undef': 15, 'MB': 9, 'NS': 6, 'NB': 4, 'SK': 2
        })

        # Gabungkan kategori dengan nilai ≤ 15 menjadi "Others"
        threshold = 15
        data_aggregated = data_analyst_province[data_analyst_province > threshold].copy()
        data_aggregated['Others'] = data_analyst_province[data_analyst_province <= threshold].sum()

        # Membuat pie chart
        ax_3.pie(
            data_aggregated,
            labels=data_aggregated.index,
            autopct='%1.1f%%',
            textprops={'color': 'white', 'fontsize': 8},
            startangle=90,
            colors=plt.cm.tab10.colors
        )

        frame3 = FigureCanvasTkAgg(figure=fig_3, master=self)
        frame3.draw()
        frame3.get_tk_widget().place(x=825, y=392)

class ToplevelWindow_3(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('Analyze Dataset')
        self.geometry("1440x1024")
        self.configure(bg="#242424")


        self.canvas = Canvas(
            self,
            bg="#242424",
            height=1024,
            width=1440,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)


        self.image_image_3 = PhotoImage(file=relative_to_assets3("image_1.png"))
        self.image_3 = self.canvas.create_image(
            720.0,
            512.0,
            image=self.image_image_3
        )
        self.resizable(False, False)

        # Option Button 2
        self.dropdown_menu_2 = customtkinter.CTkOptionMenu(master=self, 
                                                         values=["Business Analyst", "Systems Analyst", "IT Analyst", "Database Analyst", "AI Analyst", "Research Analyst", "Data Engineer"],
                                                         fg_color="#060B28", 
                                                         button_color="#060B28",
                                                         text_color="white")
        self.dropdown_menu_2.place(x=655, y=55, anchor=CENTER)  
        self.dropdown_menu_2.set("Select Column")       

        # Main Button 2
        self.main_button_2 = customtkinter.CTkButton(master=self, fg_color="#060B28", border_width=0, text_color=("White", "#DCE4EE"), text='Enter', command=self.handle_main_button2)
        self.main_button_2.place(x=815, y=55, anchor=CENTER)
        
    def handle_main_button2(self):
        self.data = pd.read_csv('Fix_Cleaned_Dataset.csv', delimiter=',', engine='python')
        selected_option = self.dropdown_menu_2.get()
        if selected_option == "Business Analyst":
            #frame 1
            city = self.data.loc[self.data[(self.data['Position'] == 'Business Analyst') & (self.data['Province'] == 'ON')].index, ['Province', 'City']].groupby('City').count()
            fig_1 = Figure(figsize=(5.8, 3.76), facecolor="#060B28")
            ax_1 = fig_1.add_subplot()
            ax_1.set_facecolor('#060B28')
            ax_1.barh(
                y=city.index,              
                width=city['Province'].values,  
                color="slateblue",          
                alpha=0.7                   
            )
            ax_1.plot(
                city['Province'].values,    
                city.index,                 
                color='violet',             
                linewidth=1.5,
                linestyle='--',              
                marker='o',                 
                markersize=4,               
                label="Peak"         
            )
            ax_1.set_title("Distribution of Business Analyst Positions by City", fontsize=10, color="white", pad=10)
            ax_1.tick_params(labelsize=5, colors='white')
            ax_1.grid(visible=True, color="gray", linestyle="--", alpha=0.5) 
            ax_1.set_xlabel("Company", fontsize=6, color="white")  
            ax_1.set_ylabel("City", fontsize=5, color="white")  
            ax_1.legend(loc="best", fontsize=6, facecolor="#060B28", edgecolor="violet", labelcolor="white")
            frame1 = FigureCanvasTkAgg(figure=fig_1, master=self)
            frame1.draw()
            frame1.get_tk_widget().place(x=788, y=110)
            #frame 2
            fig_2 = Figure(figsize=(4.5, 3.1), facecolor="#060B28")
            ax_2 = fig_2.add_subplot()
            ax_2.set_facecolor('#060B28')
            # Data untuk pie chart
            province = self.data.loc[self.data[self.data['Position']=='Business Analyst'].index, 'Province'].value_counts()
            threshold = 10
            data_aggregated = province[province > threshold].copy()
            data_aggregated['Others'] = province[province <= threshold].sum()
            ax_2.pie(
                data_aggregated,
                labels=data_aggregated.index,
                autopct='%1.1f%%',
                textprops={'color': 'white', 'fontsize': 8},
                startangle=90,
                colors=plt.cm.tab10.colors
            )
            ax_2.set_title("Distribution of Business Analyst Positions by Province", fontsize=10, color="white", pad=10)
            ax_2.legend(
                title='Province', 
                loc='lower left', 
                fontsize=4,         # Ukuran font legend
                title_fontsize=5,   # Ukuran font judul legend
                bbox_to_anchor=(0.1, 0.1)  # Posisi relative dari legend
            )
            frame2 = FigureCanvasTkAgg(figure=fig_2, master=self)
            frame2.draw()
            frame2.get_tk_widget().place(x=232, y=691)
        elif selected_option == "Systems Analyst":
            #frame 1
            city = self.data.loc[self.data[(self.data['Position'] == 'Systems Analyst') & (self.data['Province'] == 'ON')].index, ['Province', 'City']].groupby('City').count()
            fig_1 = Figure(figsize=(5.8, 3.76), facecolor="#060B28")
            ax_1 = fig_1.add_subplot()
            ax_1.set_facecolor('#060B28')
            ax_1.barh(
                y=city.index,              
                width=city['Province'].values,  
                color="slateblue",          
                alpha=0.7                   
            )
            ax_1.plot(
                city['Province'].values,    
                city.index,                 
                color='violet',             
                linewidth=1.5,
                linestyle='--',              
                marker='o',                 
                markersize=4,               
                label="Peak"         
            )
            ax_1.set_title("Distribution of Systems Analyst Positions by City", fontsize=10, color="white", pad=10)
            ax_1.tick_params(labelsize=5, colors='white')
            ax_1.grid(visible=True, color="gray", linestyle="--", alpha=0.5) 
            ax_1.set_xlabel("Company", fontsize=6, color="white")  
            ax_1.set_ylabel("City", fontsize=5, color="white")  
            ax_1.legend(loc="best", fontsize=6, facecolor="#060B28", edgecolor="violet", labelcolor="white")
            frame1 = FigureCanvasTkAgg(figure=fig_1, master=self)
            frame1.draw()
            frame1.get_tk_widget().place(x=788, y=110)
            #frame 2
            fig_2 = Figure(figsize=(4.5, 3.1), facecolor="#060B28")
            ax_2 = fig_2.add_subplot()
            ax_2.set_facecolor('#060B28')
            # Data untuk pie chart
            province = self.data.loc[self.data[self.data['Position']=='Systems Analyst'].index, 'Province'].value_counts()
            threshold = 5
            data_aggregated = province[province > threshold].copy()
            data_aggregated['Others'] = province[province <= threshold].sum()
            ax_2.pie(
                data_aggregated,
                labels=data_aggregated.index,
                autopct='%1.1f%%',
                textprops={'color': 'white', 'fontsize': 8},
                startangle=90,
                colors=plt.cm.tab10.colors
            )
            ax_2.set_title("Distribution of Systems Analyst Positions by Province", fontsize=10, color="white", pad=10)
            ax_2.legend(
                title='Province', 
                loc='lower left', 
                fontsize=4,         # Ukuran font legend
                title_fontsize=5,   # Ukuran font judul legend
                bbox_to_anchor=(0.1, 0.1)  # Posisi relative dari legend
            )
            frame2 = FigureCanvasTkAgg(figure=fig_2, master=self)
            frame2.draw()
            frame2.get_tk_widget().place(x=232, y=691)
        elif selected_option == "IT Analyst":
            #frame 1
            city = self.data.loc[self.data[(self.data['Position'] == 'IT Analyst') & (self.data['Province'] == 'ON')].index, ['Province', 'City']].groupby('City').count()
            fig_1 = Figure(figsize=(5.8, 3.76), facecolor="#060B28")
            ax_1 = fig_1.add_subplot()
            ax_1.set_facecolor('#060B28')
            ax_1.barh(
                y=city.index,              
                width=city['Province'].values,  
                color="slateblue",          
                alpha=0.7                   
            )
            ax_1.plot(
                city['Province'].values,    
                city.index,                 
                color='violet',             
                linewidth=1.5,
                linestyle='--',              
                marker='o',                 
                markersize=4,               
                label="Peak"         
            )
            ax_1.set_title("Distribution of IT Analyst Positions by City", fontsize=10, color="white", pad=10)
            ax_1.tick_params(labelsize=5, colors='white')
            ax_1.grid(visible=True, color="gray", linestyle="--", alpha=0.5) 
            ax_1.set_xlabel("Company", fontsize=6, color="white")  
            ax_1.set_ylabel("City", fontsize=5, color="white")  
            ax_1.legend(loc="best", fontsize=6, facecolor="#060B28", edgecolor="violet", labelcolor="white")
            frame1 = FigureCanvasTkAgg(figure=fig_1, master=self)
            frame1.draw()
            frame1.get_tk_widget().place(x=788, y=110)
            #frame 2
            fig_2 = Figure(figsize=(4.5, 3.1), facecolor="#060B28")
            ax_2 = fig_2.add_subplot()
            ax_2.set_facecolor('#060B28')
            # Data untuk pie chart
            province = self.data.loc[self.data[self.data['Position']=='IT Analyst'].index, 'Province'].value_counts()
            threshold = 10
            data_aggregated = province[province > threshold].copy()
            data_aggregated['Others'] = province[province <= threshold].sum()
            ax_2.pie(
                data_aggregated,
                labels=data_aggregated.index,
                autopct='%1.1f%%',
                textprops={'color': 'white', 'fontsize': 8},
                startangle=90,
                colors=plt.cm.tab10.colors
            )
            ax_2.set_title("Distribution of IT Analyst Positions by Province", fontsize=10, color="white", pad=10)
            ax_2.legend(
                title='Province', 
                loc='lower left', 
                fontsize=4,         # Ukuran font legend
                title_fontsize=5,   # Ukuran font judul legend
                bbox_to_anchor=(0.1, 0.1)  # Posisi relative dari legend
            )
            frame2 = FigureCanvasTkAgg(figure=fig_2, master=self)
            frame2.draw()
            frame2.get_tk_widget().place(x=232, y=691)
        elif selected_option == "Database Analyst":
            #frame 1
            city = self.data.loc[self.data[(self.data['Position'] == 'Database Analyst') & (self.data['Province'] == 'ON')].index, ['Province', 'City']].groupby('City').count()
            fig_1 = Figure(figsize=(5.8, 3.76), facecolor="#060B28")
            ax_1 = fig_1.add_subplot()
            ax_1.set_facecolor('#060B28')
            ax_1.barh(
                y=city.index,              
                width=city['Province'].values,  
                color="slateblue",          
                alpha=0.7                   
            )
            ax_1.plot(
                city['Province'].values,    
                city.index,                 
                color='violet',             
                linewidth=1.5,
                linestyle='--',              
                marker='o',                 
                markersize=4,               
                label="Peak"         
            )
            ax_1.set_title("Distribution of Database Analyst Positions by City", fontsize=10, color="white", pad=10)
            ax_1.tick_params(labelsize=5, colors='white')
            ax_1.grid(visible=True, color="gray", linestyle="--", alpha=0.5) 
            ax_1.set_xlabel("Company", fontsize=6, color="white")  
            ax_1.set_ylabel("City", fontsize=5, color="white")  
            ax_1.legend(loc="best", fontsize=6, facecolor="#060B28", edgecolor="violet", labelcolor="white")
            frame1 = FigureCanvasTkAgg(figure=fig_1, master=self)
            frame1.draw()
            frame1.get_tk_widget().place(x=788, y=110)
            #frame 2
            fig_2 = Figure(figsize=(4.5, 3.1), facecolor="#060B28")
            ax_2 = fig_2.add_subplot()
            ax_2.set_facecolor('#060B28')
            # Data untuk pie chart
            province = self.data.loc[self.data[self.data['Position']=='Database Analyst'].index, 'Province'].value_counts()
            threshold = 2
            data_aggregated = province[province > threshold].copy()
            data_aggregated['Others'] = province[province <= threshold].sum()
            ax_2.pie(
                data_aggregated,
                labels=data_aggregated.index,
                autopct='%1.1f%%',
                textprops={'color': 'white', 'fontsize': 8},
                startangle=90,
                colors=plt.cm.tab10.colors
            )
            ax_2.set_title("Distribution of Database Analyst Positions by Province", fontsize=10, color="white", pad=10)
            ax_2.legend(
                title='Province', 
                loc='lower left', 
                fontsize=4,         # Ukuran font legend
                title_fontsize=5,   # Ukuran font judul legend
                bbox_to_anchor=(0.1, 0.1)  # Posisi relative dari legend
            )
            frame2 = FigureCanvasTkAgg(figure=fig_2, master=self)
            frame2.draw()
            frame2.get_tk_widget().place(x=232, y=691)
        elif selected_option == "AI Analyst":
            #frame 1
            city = self.data.loc[self.data[(self.data['Position'] == 'AI Analyst') & (self.data['Province'] == 'ON')].index, ['Province', 'City']].groupby('City').count()
            fig_1 = Figure(figsize=(5.8, 3.76), facecolor="#060B28")
            ax_1 = fig_1.add_subplot()
            ax_1.set_facecolor('#060B28')
            ax_1.barh(
                y=city.index,              
                width=city['Province'].values,  
                color="slateblue",          
                alpha=0.7                   
            )
            ax_1.plot(
                city['Province'].values,    
                city.index,                 
                color='violet',             
                linewidth=1.5,
                linestyle='--',              
                marker='o',                 
                markersize=4,               
                label="Peak"         
            )
            ax_1.set_title("Distribution of AI Analyst Positions by City", fontsize=10, color="white", pad=10)
            ax_1.tick_params(labelsize=5, colors='white')
            ax_1.grid(visible=True, color="gray", linestyle="--", alpha=0.5) 
            ax_1.set_xlabel("Company", fontsize=6, color="white")  
            ax_1.set_ylabel("City", fontsize=5, color="white")  
            ax_1.legend(loc="best", fontsize=6, facecolor="#060B28", edgecolor="violet", labelcolor="white")
            frame1 = FigureCanvasTkAgg(figure=fig_1, master=self)
            frame1.draw()
            frame1.get_tk_widget().place(x=788, y=110)
            #frame 2
            fig_2 = Figure(figsize=(4.5, 3.1), facecolor="#060B28")
            ax_2 = fig_2.add_subplot()
            ax_2.set_facecolor('#060B28')
            # Data untuk pie chart
            province = self.data.loc[self.data[self.data['Position']=='AI Analyst'].index, 'Province'].value_counts()
            threshold = 4
            data_aggregated = province[province > threshold].copy()
            data_aggregated['Others'] = province[province <= threshold].sum()
            ax_2.pie(
                data_aggregated,
                labels=data_aggregated.index,
                autopct='%1.1f%%',
                textprops={'color': 'white', 'fontsize': 8},
                startangle=90,
                colors=plt.cm.tab10.colors
            )
            ax_2.set_title("Distribution of AI Analyst Positions by Province", fontsize=10, color="white", pad=10)
            ax_2.legend(
                title='Province', 
                loc='lower left', 
                fontsize=4,         # Ukuran font legend
                title_fontsize=5,   # Ukuran font judul legend
                bbox_to_anchor=(0.1, 0.1)  # Posisi relative dari legend
            )
            frame2 = FigureCanvasTkAgg(figure=fig_2, master=self)
            frame2.draw()
            frame2.get_tk_widget().place(x=232, y=691)
        elif selected_option == "Research Analyst":
            #frame 1
            city = self.data.loc[self.data[(self.data['Position'] == 'Research Analyst') & (self.data['Province'] == 'ON')].index, ['Province', 'City']].groupby('City').count()
            fig_1 = Figure(figsize=(5.8, 3.76), facecolor="#060B28")
            ax_1 = fig_1.add_subplot()
            ax_1.set_facecolor('#060B28')
            ax_1.barh(
                y=city.index,              
                width=city['Province'].values,  
                color="slateblue",          
                alpha=0.7                   
            )
            ax_1.plot(
                city['Province'].values,    
                city.index,                 
                color='violet',             
                linewidth=1.5,
                linestyle='--',              
                marker='o',                 
                markersize=4,               
                label="Peak"         
            )
            ax_1.set_title("Distribution of Research Analyst Positions by City", fontsize=10, color="white", pad=10)
            ax_1.tick_params(labelsize=5, colors='white')
            ax_1.grid(visible=True, color="gray", linestyle="--", alpha=0.5) 
            ax_1.set_xlabel("Company", fontsize=6, color="white")  
            ax_1.set_ylabel("City", fontsize=5, color="white")  
            ax_1.legend(loc="best", fontsize=6, facecolor="#060B28", edgecolor="violet", labelcolor="white")
            frame1 = FigureCanvasTkAgg(figure=fig_1, master=self)
            frame1.draw()
            frame1.get_tk_widget().place(x=788, y=110)
            #frame 2
            fig_2 = Figure(figsize=(4.5, 3.1), facecolor="#060B28")
            ax_2 = fig_2.add_subplot()
            ax_2.set_facecolor('#060B28')
            # Data untuk pie chart
            province = self.data.loc[self.data[self.data['Position']=='Research Analyst'].index, 'Province'].value_counts()
            threshold = 4
            data_aggregated = province[province > threshold].copy()
            data_aggregated['Others'] = province[province <= threshold].sum()
            ax_2.pie(
                data_aggregated,
                labels=data_aggregated.index,
                autopct='%1.1f%%',
                textprops={'color': 'white', 'fontsize': 8},
                startangle=90,
                colors=plt.cm.tab10.colors
            )
            ax_2.set_title("Distribution of Research Analyst Positions by Province", fontsize=10, color="white", pad=10)
            ax_2.legend(
                title='Province', 
                loc='lower left', 
                fontsize=4,         # Ukuran font legend
                title_fontsize=5,   # Ukuran font judul legend
                bbox_to_anchor=(0.1, 0.1)  # Posisi relative dari legend
            )
            frame2 = FigureCanvasTkAgg(figure=fig_2, master=self)
            frame2.draw()
            frame2.get_tk_widget().place(x=232, y=691)
        elif selected_option == "Data Engineer":
            #frame 1
            city = self.data.loc[self.data[(self.data['Position'] == 'Data Engineer') & (self.data['Province'] == 'ON')].index, ['Province', 'City']].groupby('City').count()
            fig_1 = Figure(figsize=(5.8, 3.76), facecolor="#060B28")
            ax_1 = fig_1.add_subplot()
            ax_1.set_facecolor('#060B28')
            ax_1.barh(
                y=city.index,              
                width=city['Province'].values,  
                color="slateblue",          
                alpha=0.7                   
            )
            ax_1.plot(
                city['Province'].values,    
                city.index,                 
                color='violet',             
                linewidth=1.5,
                linestyle='--',              
                marker='o',                 
                markersize=4,               
                label="Peak"         
            )
            ax_1.set_title("Distribution of Data Engineer Positions by City", fontsize=10, color="white", pad=10)
            ax_1.tick_params(labelsize=5, colors='white')
            ax_1.grid(visible=True, color="gray", linestyle="--", alpha=0.5) 
            ax_1.set_xlabel("Company", fontsize=6, color="white")  
            ax_1.set_ylabel("City", fontsize=5, color="white")  
            ax_1.legend(loc="best", fontsize=6, facecolor="#060B28", edgecolor="violet", labelcolor="white")
            frame1 = FigureCanvasTkAgg(figure=fig_1, master=self)
            frame1.draw()
            frame1.get_tk_widget().place(x=788, y=110)
            #frame 2
            fig_2 = Figure(figsize=(4.5, 3.1), facecolor="#060B28")
            ax_2 = fig_2.add_subplot()
            ax_2.set_facecolor('#060B28')
            # Data untuk pie chart
            province = self.data.loc[self.data[self.data['Position']=='Data Engineer'].index, 'Province'].value_counts()
            threshold = 4
            data_aggregated = province[province > threshold].copy()
            data_aggregated['Others'] = province[province <= threshold].sum()
            ax_2.pie(
                data_aggregated,
                labels=data_aggregated.index,
                autopct='%1.1f%%',
                textprops={'color': 'white', 'fontsize': 8},
                startangle=90,
                colors=plt.cm.tab10.colors
            )
            ax_2.set_title("Distribution of Data Engineer Positions by Province", fontsize=10, color="white", pad=10)
            ax_2.legend(
                title='Province', 
                loc='lower left', 
                fontsize=4,         # Ukuran font legend
                title_fontsize=5,   # Ukuran font judul legend
                bbox_to_anchor=(0.1, 0.1)  # Posisi relative dari legend
            )
            frame2 = FigureCanvasTkAgg(figure=fig_2, master=self)
            frame2.draw()
            frame2.get_tk_widget().place(x=232, y=691)
        else:
            tkinter.messagebox.showwarning("No Selection", "Please select an option from the dropdown.")
        
class DataAnalystApp(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title('Analyze Dataset')
        self.geometry("1428x1007")
        self.configure(bg="#f0f0f0")

        self.toplevelwindow_1 = None
        self.toplevelwindow_2 = None
        self.toplevelwindow_3 = None


        # Canvas for Background
        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.canvas.pack(fill=BOTH, expand=True)

        # Load Background Image
        try:
            self.bg_image = Image.open("bg fix.png")  
            self.bg_photo = ImageTk.PhotoImage(self.bg_image)
            self.bg_canvas_image = self.canvas.create_image(0, 0, image=self.bg_photo, anchor=NW)

            
        except FileNotFoundError:
            tkinter.messagebox.showerror("Error", "background.jpg not found. Please check the file path.")

        # Load Logo
        try:
            my_image = customtkinter.CTkImage(light_image=Image.open("Logo.png"),
                                              dark_image=Image.open("Logo.png"),
                                              size=(300, 300))  
            image_label = customtkinter.CTkLabel(master=self, image=my_image, text="")
            image_label.place(relx=0.5, rely=0.2, anchor=CENTER)  
        except FileNotFoundError:
            tkinter.messagebox.showerror("Error", "Logo.png not found. Please check the file path.")


        #Font
        custom_font = customtkinter.CTkFont(family="Times New Roman", size=96, weight="bold", slant="italic")

         # Greeting Text
        self.label_greeting = customtkinter.CTkLabel(master=self,
                                                    text="Hello, Ryan.",
                                                    font=custom_font,
                                                    text_color="white")
        self.label_greeting.place(relx=0.5, rely=0.4, anchor=CENTER)

        # Sub-Greeting
        self.sublabel_greeting = customtkinter.CTkLabel(master=self,
                                                text="How can I help you?",
                                                font=("Bahnschrift SemiBold", 24),
                                                text_color="gray")
        self.sublabel_greeting.place(relx=0.5, rely=0.5, anchor=CENTER)   

        # Option Button 1
        self.dropdown_menu_1 = customtkinter.CTkOptionMenu(master=self, 
                                                         values=["Display Dataset", "Dashboard Statistics", "Analyze Dataset"],
                                                         fg_color="#242424", 
                                                         button_color="#242424",
                                                         text_color="white")
        self.dropdown_menu_1.place(relx=0.5, rely=0.55, anchor=CENTER)  
        self.dropdown_menu_1.set("Select Option")       

        # Main Button 1
        self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=1, text_color=("gray10", "#DCE4EE"), text='Enter', command=self.handle_main_button)
        self.main_button_1.place(relx=0.5, rely=0.59, anchor=CENTER)

    def handle_main_button(self):
        selected_option = self.dropdown_menu_1.get()
        if selected_option == "Display Dataset":
            self.open_toplevel_window_1()
        elif selected_option == "Dashboard Statistics":
            self.open_toplevel_window_2()
        elif selected_option == "Analyze Dataset":
            self.open_toplevel_window_3()
        else:
            tkinter.messagebox.showwarning("No Selection", "Please select an option from the dropdown.")

    def open_toplevel_window_1(self):
        if self.toplevelwindow_1 is None or not self.toplevelwindow_1.winfo_exists():
            self.toplevelwindow_1 = ToplevelWindow_1(self)
            self.toplevelwindow_1.display_dataset()
        else:
            self.toplevelwindow_1.focus()

    def open_toplevel_window_2(self):
        if self.toplevelwindow_2 is None or not self.toplevelwindow_2.winfo_exists():
            self.toplevelwindow_2 = ToplevelWindow_2(self)
            self.toplevelwindow_2.display_dataset2()
        else:
            self.toplevelwindow_2.focus()

    def open_toplevel_window_3(self):
        if self.toplevelwindow_3 is None or not self.toplevelwindow_3.winfo_exists():
            self.toplevelwindow_3 = ToplevelWindow_3(self)
        else:
            self.toplevelwindow_3.focus()

if __name__ == "__main__":
    app = DataAnalystApp()
    app.mainloop()
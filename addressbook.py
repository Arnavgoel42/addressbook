import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
import tempfile
import webbrowser

# --- Data folder and files ---
DATA_FOLDER = "data"
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

USER_FILE = os.path.join(DATA_FOLDER, "users.csv")
ADDRESS_FILE = os.path.join(DATA_FOLDER, "address_book.csv")
RECYCLE_FILE = os.path.join(DATA_FOLDER, "recycle_bin.csv")

USER_FIELDS = ["Username", "Email", "Mobile", "Password"]
ADDRESS_FIELDS = [
    "Name", "Phone", "Email", "Address", "City",
    "State", "Pincode", "Country", "Type"
]

# --- Indian States ---
INDIAN_STATES = [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
    "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand",
    "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur",
    "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab", "Rajasthan",
    "Sikkim", "Tamil Nadu", "Telangana", "Tripura", "Uttar Pradesh",
    "Uttarakhand", "West Bengal", "Andaman and Nicobar Islands",
    "Chandigarh", "Dadra and Nagar Haveli and Daman and Diu", "Delhi",
    "Jammu & Kashmir", "Ladakh", "Lakshadweep", "Puducherry"
]

# --- Countries ---
COUNTRIES = [
    # List shortened for brevity; expand as needed
    "Afghanistan","Albania","Algeria","Andorra","Angola","Argentina","Armenia","Australia","Austria","Azerbaijan",
    "Bahamas","Bahrain","Bangladesh","Barbados","Belarus","Belgium","Belize","Bhutan","Bolivia","Bosnia and Herzegovina",
    "Brazil","Brunei","Bulgaria","Burkina Faso","Burundi","Cambodia","Cameroon","Canada","Cape Verde","Central African Republic",
    "Chad","Chile","China","Colombia","Comoros","Congo (Brazzaville)","Congo (Kinshasa)","Costa Rica","Croatia","Cuba",
    "Cyprus","Czech Republic","Denmark","Djibouti","Dominica","Dominican Republic","East Timor","Ecuador","Egypt","El Salvador",
    "Equatorial Guinea","Eritrea","Estonia","Ethiopia","Fiji","Finland","France","Gabon","Gambia","Georgia","Germany","Ghana",
    "Greece","Grenada","Guatemala","Guinea","Guinea-Bissau","Guyana","Haiti","Honduras","Hungary","Iceland","India","Indonesia",
    "Iran","Iraq","Ireland","Israel","Italy","Jamaica","Japan","Jordan","Kazakhstan","Kenya","Kiribati","Korea, North","Korea, South",
    "Kuwait","Kyrgyzstan","Laos","Latvia","Lebanon","Lesotho","Liberia","Libya","Liechtenstein","Lithuania","Luxembourg","Madagascar",
    "Malawi","Malaysia","Maldives","Mali","Malta","Marshall Islands","Mauritania","Mauritius","Mexico","Micronesia","Moldova",
    "Monaco","Montenegro","Morocco","Mozambique","Myanmar","Namibia","Nauru","Nepal","Netherlands","New Zealand","Nicaragua",
    "Niger","Nigeria","Norway","Oman","Pakistan","Palau","Panama","Papua New Guinea","Paraguay","Peru","Philippines","Poland",
    "Portugal","Qatar","Romania","Russia","Rwanda","Saint Kitts and Nevis","Saint Lucia","Saint Vincent and the Grenadines","Samoa",
    "San Marino","Sao Tome and Principe","Saudi Arabia","Senegal","Serbia","Seychelles","Sierra Leone","Singapore","Slovakia",
    "Slovenia","Solomon Islands","Somalia","South Africa","Spain","Sri Lanka","Sudan","Suriname","Swaziland","Sweden","Switzerland",
    "Syria","Taiwan","Tajikistan","Tanzania","Thailand","Togo","Tonga","Trinidad and Tobago","Tunisia","Turkey","Turkmenistan",
    "Tuvalu","Uganda","Ukraine","United Arab Emirates","United Kingdom","United States","Uruguay","Uzbekistan","Vanuatu",
    "Vatican City","Venezuela","Vietnam","Yemen","Zambia","Zimbabwe"
]

# --- Styles ---
ENTRY_BG = "#f0f4f8"
PRIMARY_COLOR = "#1976D2"
SECONDARY_COLOR = "#42A5F5"
DANGER_COLOR = "#E53935"
SUCCESS_COLOR = "#388E3C"
RECYCLE_BG = "#ffe9cc"
FONT_TITLE = ('Segoe UI', 11, 'bold')
FONT_LABEL = ('Segoe UI', 10)
FONT_BTN = ('Segoe UI', 10, 'bold')
FONT_HEADER = ('Segoe UI', 16, 'bold')


# --- Utility functions ---

def read_csv(filename):
    if os.path.exists(filename):
        with open(filename, newline='', encoding='utf-8') as f:
            return list(csv.DictReader(f))
    return []


def write_csv(filename, data, fields):
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(data)


def show_print(entries):
    if not entries:
        messagebox.showinfo("No Entries", "No entries to print.")
        return

    html = "<html><body><h2>Address Book - Print Preview</h2>"
    for entry in entries:
        html += "<div style='border:1px solid #ccc; margin:10px; padding:10px;'>"
        for k in ADDRESS_FIELDS:
            html += f"<b>{k}:</b> {entry[k]}<br>"
        html += "</div>"
    html += "<script>window.print();</script></body></html>"

    with tempfile.NamedTemporaryFile('w', delete=False, suffix=".html", encoding='utf-8') as f:
        f.write(html)
        webbrowser.open(f.name)


class AddressBookApp:
    def __init__(self, root):
        self.root = root

        self.user = None
        self.user_info = None

        self.widgets = {}
        self.tab_widgets = []
        self.entries_frame = None
        self.recycle_window = None

        self.setup_styles()
        self.setup_ui()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure(
            "TCombobox",
            fieldbackground=ENTRY_BG,
            background="white",
            relief='flat',
            padding=5,
            font=FONT_LABEL,
        )
        style.configure(
            "Accent.TButton",
            background=PRIMARY_COLOR,
            foreground="white",
            font=FONT_BTN,
        )
        style.map("Accent.TButton", background=[('active', SECONDARY_COLOR)])

    def setup_ui(self):
        topbar = tk.Frame(self.root, bg="#e3f4fd", height=48)
        topbar.pack(side='top', fill='x')

        self.auth_btn = tk.Menubutton(
            topbar,
            text="Login/Sign-up",
            bg=PRIMARY_COLOR,
            fg='white',
            font=FONT_BTN,
            relief='flat',
            activebackground=SECONDARY_COLOR,
            activeforeground='white'
        )
        self.auth_btn.menu = tk.Menu(self.auth_btn, font=FONT_LABEL, tearoff=0)
        self.auth_btn['menu'] = self.auth_btn.menu
        self.auth_btn.menu.add_command(label="Login/Sign-up", command=self.show_login_signup)
        self.auth_btn.pack(side='right', padx=10, pady=5)

        self.topbar = topbar

        self.main_frame = tk.Frame(self.root, bg="white")
        self.main_frame.pack(fill='both', expand=True, padx=20, pady=15)

        # Start with login/signup view
        self.show_login_signup()

    def clear_main(self):
        for w in self.main_frame.winfo_children():
            w.destroy()

    # --- Authentication --- #
    def show_login_signup(self):
        self.clear_main()

        frame = tk.Frame(self.main_frame, bg="white")
        frame.pack(expand=True)
        content = tk.Frame(frame, bg="white", padx=150, pady=40)
        content.pack(expand=True)

        label_header = tk.Label(
            content,
            text="Welcome! Please Login or Sign-up to use your Secure Address Book",
            font=FONT_HEADER,
            fg=PRIMARY_COLOR,
            bg="white",
            wraplength=450,
            justify='center'
        )
        label_header.pack(pady=(0, 30))

        tabs = ttk.Notebook(content)
        tabs.pack(expand=True, fill='both')

        self._build_login_tab(tabs)
        self._build_signup_tab(tabs)
        self._build_forgot_tab(tabs)

    def _build_login_tab(self, notebook):
        login_tab = tk.Frame(notebook, bg='white', padx=20, pady=20)
        notebook.add(login_tab, text="Login")

        labels = ["Username", "Password"]
        self.login_entries = {}

        for idx, label in enumerate(labels):
            tk.Label(login_tab, text=label+":", font=FONT_LABEL, bg='white').grid(row=idx, column=0, pady=8, sticky='w')
            ent = tk.Entry(login_tab, font=FONT_LABEL, width=32, bg=ENTRY_BG, relief='solid', bd=1)
            if label == "Password":
                ent.config(show="*")
            ent.grid(row=idx, column=1, pady=8)
            self.login_entries[label] = ent

        login_btn = tk.Button(
            login_tab,
            text="Login",
            font=FONT_BTN,
            bg=SUCCESS_COLOR,
            fg='white',
            padx=25,
            pady=10,
            relief='flat',
            command=self.login
        )
        login_btn.grid(row=len(labels), column=0, columnspan=2, pady=20, sticky='ew')

    def _build_signup_tab(self, notebook):
        signup_tab = tk.Frame(notebook, bg='white', padx=20, pady=20)
        notebook.add(signup_tab, text="Sign-up")

        labels = ["Username", "Email", "Mobile", "Password"]
        self.signup_entries = {}

        for idx, label in enumerate(labels):
            tk.Label(signup_tab, text=label+":", font=FONT_LABEL, bg='white').grid(row=idx, column=0, pady=8, sticky='w')
            ent = tk.Entry(signup_tab, font=FONT_LABEL, width=32, bg=ENTRY_BG, relief='solid', bd=1)
            if label == "Password":
                ent.config(show="*")
            ent.grid(row=idx, column=1, pady=8)
            self.signup_entries[label] = ent

        signup_btn = tk.Button(
            signup_tab,
            text="Sign-up",
            font=FONT_BTN,
            bg=SUCCESS_COLOR,
            fg='white',
            relief='flat',
            command=self.signup
        )
        signup_btn.grid(row=len(labels), column=0, columnspan=2, pady=20, sticky='ew')

    def _build_forgot_tab(self, notebook):
        forgot_tab = tk.Frame(notebook, bg='white', padx=20, pady=20)
        notebook.add(forgot_tab, text="Forgot Password")

        tk.Label(forgot_tab, text="Username:", font=FONT_LABEL, bg='white').grid(row=0, column=0, pady=8, sticky='w')
        self.forgot_username = tk.Entry(forgot_tab, font=FONT_LABEL, width=32, bg=ENTRY_BG, relief='solid', bd=1)
        self.forgot_username.grid(row=0, column=1, pady=8)

        self.forgot_verify_btn = tk.Button(
            forgot_tab,
            text="Verify",
            font=FONT_BTN,
            bg=PRIMARY_COLOR,
            fg='white',
            relief='flat',
            command=self.forgot_verify
        )
        self.forgot_verify_btn.grid(row=1, column=0, columnspan=2, pady=12, sticky='ew')

        self.forgot_newpw_lbl = tk.Label(forgot_tab, text="New Password:", font=FONT_LABEL, bg='white')
        self.forgot_newpw_entry = tk.Entry(forgot_tab, font=FONT_LABEL, width=32, bg=ENTRY_BG, relief='solid', bd=1, show='*')

        self.forgot_confpw_lbl = tk.Label(forgot_tab, text="Confirm Password:", font=FONT_LABEL, bg='white')
        self.forgot_confpw_entry = tk.Entry(forgot_tab, font=FONT_LABEL, width=32, bg=ENTRY_BG, relief='solid', bd=1, show='*')

        self.forgot_update_btn = tk.Button(
            forgot_tab,
            text="Update Password",
            font=FONT_BTN,
            bg=SUCCESS_COLOR,
            fg='white',
            relief='flat',
            command=self.forgot_update
        )

        for widget in (self.forgot_newpw_lbl,
                       self.forgot_newpw_entry,
                       self.forgot_confpw_lbl,
                       self.forgot_confpw_entry,
                       self.forgot_update_btn):
            widget.grid_remove()

    def login(self):
        username = self.login_entries["Username"].get().strip()
        password = self.login_entries["Password"].get()
        if not username or not password:
            messagebox.showerror("Error", "All fields are required.", parent=self.root)
            return

        users = read_csv(USER_FILE)
        user = next((u for u in users if u["Username"].lower() == username.lower() and u["Password"] == password), None)

        if user:
            self.user = user["Username"]
            self.user_info = user
            self.auth_btn.config(text=self.user)
            self.auth_btn.menu.delete(0, 'end')
            self.auth_btn.menu.add_command(label="Profile", command=self.show_profile)
            self.auth_btn.menu.add_command(label="Logout", command=self.logout)
            self.auth_btn.menu.add_command(label="Delete Account", command=self.delete_account)
            messagebox.showinfo("Success", f"Welcome, {self.user}!", parent=self.root)
            self.show_address_book()
        else:
            messagebox.showerror("Failed", "Invalid username or password.", parent=self.root)

    def signup(self):
        data = {k: v.get().strip() for k, v in self.signup_entries.items()}
        if not all(data.values()):
            messagebox.showerror("Error", "All fields are required.", parent=self.root)
            return

        users = read_csv(USER_FILE)
        if any(u["Username"].lower() == data["Username"].lower() for u in users):
            messagebox.showerror("Error", "Username already exists.", parent=self.root)
            return
        if any(u["Email"].lower() == data["Email"].lower() for u in users):
            messagebox.showerror("Error", "Email already registered.", parent=self.root)
            return
        if any(u["Mobile"] == data["Mobile"] for u in users):
            messagebox.showerror("Error", "Mobile number already registered.", parent=self.root)
            return

        users.append(data)
        write_csv(USER_FILE, users, USER_FIELDS)

        messagebox.showinfo("Success", "Account created! Logged in automatically.", parent=self.root)

        self.user = data["Username"]
        self.user_info = data
        self.auth_btn.config(text=self.user)
        self.auth_btn.menu.delete(0, 'end')
        self.auth_btn.menu.add_command(label="Profile", command=self.show_profile)
        self.auth_btn.menu.add_command(label="Logout", command=self.logout)
        self.auth_btn.menu.add_command(label="Delete Account", command=self.delete_account)

        self.show_address_book()

    def forgot_verify(self):
        username = self.forgot_username.get().strip()
        if not username:
            messagebox.showerror("Error", "Please enter your username.", parent=self.root)
            return
        users = read_csv(USER_FILE)
        self.forgot_user = next((u for u in users if u["Username"].lower() == username.lower()), None)
        if self.forgot_user:
            self.forgot_verify_btn['state'] = 'disabled'
            self.forgot_username['state'] = 'readonly'
            self.forgot_newpw_lbl.grid(row=2, column=0, pady=8, sticky='w')
            self.forgot_newpw_entry.grid(row=2, column=1, pady=8)
            self.forgot_confpw_lbl.grid(row=3, column=0, pady=8, sticky='w')
            self.forgot_confpw_entry.grid(row=3, column=1, pady=8)
            self.forgot_update_btn.grid(row=4, column=0, columnspan=2, pady=15, sticky='ew')
        else:
            messagebox.showerror("Error", "Username not found.", parent=self.root)

    def forgot_update(self):
        new_pw = self.forgot_newpw_entry.get()
        conf_pw = self.forgot_confpw_entry.get()
        if not new_pw or not conf_pw:
            messagebox.showerror("Error", "Both password fields are required.", parent=self.root)
            return
        if new_pw != conf_pw:
            messagebox.showerror("Error", "Passwords do not match.", parent=self.root)
            return

        users = read_csv(USER_FILE)
        for idx, u in enumerate(users):
            if u["Username"].lower() == self.forgot_user["Username"].lower():
                users[idx]["Password"] = new_pw
                write_csv(USER_FILE, users, USER_FIELDS)
                messagebox.showinfo("Success", "Password changed successfully.", parent=self.root)
                self.show_login_signup()
                break

    def logout(self):
        self.user = None
        self.user_info = None
        self.auth_btn.config(text="Login/Sign-up")
        self.auth_btn.menu.delete(0, 'end')
        self.auth_btn.menu.add_command(label="Login/Sign-up", command=self.show_login_signup)
        self.show_login_signup()

    def delete_account(self):
        if messagebox.askyesno("Confirm", "Delete your account? This cannot be undone.", parent=self.root):
            users = read_csv(USER_FILE)
            users = [u for u in users if u["Username"].lower() != self.user.lower()]
            write_csv(USER_FILE, users, USER_FIELDS)
            messagebox.showinfo("Deleted", "Your account was deleted.", parent=self.root)
            self.logout()

    def show_profile(self):
        profile_win = tk.Toplevel(self.root)
        profile_win.title("Profile")
        profile_win.geometry("440x470")
        profile_win.configure(bg='white')

        fields = ["Username", "Email", "Mobile", "Old Password", "New Password"]
        entries = {}

        for i, field in enumerate(fields):
            tk.Label(profile_win, text=field + ':', font=FONT_LABEL, bg='white').grid(row=i, column=0, padx=15, pady=10, sticky='w')
            ent = tk.Entry(profile_win, font=FONT_LABEL, width=32, bg=ENTRY_BG, relief='solid', bd=1)
            if 'Password' in field:
                ent.config(show='*')
            if self.user_info and field in self.user_info and "Password" not in field:
                ent.insert(0, self.user_info[field])
            ent.grid(row=i, column=1, padx=15, pady=10)
            entries[field] = ent

        def save_profile():
            uname = entries["Username"].get().strip()
            email = entries["Email"].get().strip()
            mobile = entries["Mobile"].get().strip()
            old_pw = entries["Old Password"].get()
            new_pw = entries["New Password"].get()

            if not uname or not email or not mobile:
                messagebox.showerror("Error", "Username, Email, and Mobile are required.", parent=profile_win)
                return
            users = read_csv(USER_FILE)
            idx = next((i for i,u in enumerate(users) if u["Username"].lower() == self.user.lower()), None)
            if idx is None:
                messagebox.showerror("Error", "User not found.", parent=profile_win)
                return

            for i, u in enumerate(users):
                if i != idx:
                    if u["Username"].lower() == uname.lower():
                        messagebox.showerror("Error", "Username already taken.", parent=profile_win)
                        return
                    if u["Email"].lower() == email.lower():
                        messagebox.showerror("Error", "Email already taken.", parent=profile_win)
                        return
                    if u["Mobile"] == mobile:
                        messagebox.showerror("Error", "Mobile number already taken.", parent=profile_win)
                        return

            if new_pw:
                if not old_pw:
                    messagebox.showerror("Error", "Please provide your current password to set a new password.", parent=profile_win)
                    return
                if users[idx]["Password"] != old_pw:
                    messagebox.showerror("Error", "Current password is incorrect.", parent=profile_win)
                    return
                users[idx]["Password"] = new_pw

            users[idx]["Username"] = uname
            users[idx]["Email"] = email
            users[idx]["Mobile"] = mobile

            write_csv(USER_FILE, users, USER_FIELDS)

            self.user = uname
            self.user_info = users[idx]

            self.auth_btn.config(text=self.user)
            messagebox.showinfo("Success", "Profile updated.", parent=profile_win)
            profile_win.destroy()

        save_btn = tk.Button(profile_win, text="Update", font=FONT_BTN, bg=PRIMARY_COLOR, fg='white', relief='flat', command=save_profile)
        save_btn.grid(row=len(fields), column=0, columnspan=2, pady=20, padx=12, sticky='ew')

    # --- Address Book ---

    def show_address_book(self):
        self.clear_main()

        top_bar_frame = tk.Frame(self.main_frame, bg='white')
        top_bar_frame.pack(fill='x')

        btn_recycle = tk.Button(top_bar_frame,
                                text="Recycle Bin",
                                bg='#FFA726', fg='white', font=FONT_BTN,
                                relief='flat', command=self.open_recycle_bin)
        btn_recycle.pack(side='right', padx=6, pady=6)

        btn_print = tk.Button(top_bar_frame,
                              text="Print All",
                              bg='#7E57C2', fg='white', font=FONT_BTN,
                              relief='flat', command=lambda: show_print(read_csv(ADDRESS_FILE)))
        btn_print.pack(side='right', padx=6, pady=6)

        btn_delete_all = tk.Button(top_bar_frame,
                                   text="Delete All",
                                   bg='#789C9C', fg='white', font=FONT_BTN,
                                   relief='flat', command=self.delete_all_entries)
        btn_delete_all.pack(side='right', padx=6, pady=6)

        btn_exit = tk.Button(top_bar_frame,
                             text="Exit",
                             bg=DANGER_COLOR, fg='white', font=FONT_BTN,
                             relief='flat', command=self.root.quit)
        btn_exit.pack(side='right', padx=6, pady=6)

        container = tk.Frame(self.main_frame, bg="white")
        container.pack(fill='both', expand=True, pady=(10, 0))

        container.columnconfigure(0, weight=1)
        container.columnconfigure(1, weight=3)

        self.build_form(container)
        self.build_address_list(container)

    def build_form(self, parent):
        form_frame = tk.LabelFrame(parent, text="Add New Entry",
                                   bg='white',
                                   font=FONT_TITLE,
                                   relief='groove')
        form_frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
        form_frame.columnconfigure(1, weight=1)

        self.widgets.clear()
        self.tab_widgets.clear()

        for i, field in enumerate(ADDRESS_FIELDS):
            lbl = tk.Label(form_frame, text=field + ":",
                           font=FONT_LABEL,
                           bg='white')
            lbl.grid(row=i, column=0, sticky='w', padx=10, pady=6)
            widget = self.make_widget_for_field(form_frame, field)
            widget.grid(row=i, column=1, sticky='ew', padx=10, pady=2)
            self.widgets[field] = widget
            self.tab_widgets.append(widget)

        save_btn = tk.Button(form_frame,
                             text="Save Entry",
                             font=FONT_BTN,
                             bg=SECONDARY_COLOR,
                             fg='white',
                             relief='flat',
                             command=self.save_entry)
        save_btn.grid(row=len(ADDRESS_FIELDS), column=0,
                      columnspan=2,
                      pady=16,
                      padx=10,
                      sticky='ew')

        # Navigation keys for form
        for idx, widget in enumerate(self.tab_widgets):
            def handler(event, index=idx):
                self.focus_next_field(index)
                return "break"
            if isinstance(widget, tk.Text):
                widget.bind("<Control-Return>", handler)
                widget.bind("<Shift-Return>", handler)
                widget.bind("<Return>", lambda e: None)
            else:
                widget.bind("<Return>", handler)

    def make_widget_for_field(self, parent, field):
        if field == "Address":
            text = tk.Text(parent, height=3, width=28,
                           font=FONT_LABEL,
                           bg=ENTRY_BG,
                           relief='flat',
                           highlightthickness=1,
                           highlightbackground='#c0c0c0')
            return text
        elif field == "State":
            combo = ttk.Combobox(parent,
                                 values=INDIAN_STATES,
                                 width=25,
                                 font=FONT_LABEL)
            combo.set("Delhi")
            return combo
        elif field == "Country":
            combo = ttk.Combobox(parent,
                                 values=COUNTRIES,
                                 width=25,
                                 font=FONT_LABEL)
            combo.set("India")
            return combo
        elif field == "Type":
            combo = ttk.Combobox(parent,
                                 values=["Personal", "Business"],
                                 width=25,
                                 font=FONT_LABEL)
            combo.set("Personal")
            return combo
        else:
            ent = tk.Entry(parent,
                           width=30,
                           font=FONT_LABEL,
                           bg=ENTRY_BG,
                           relief='flat',
                           highlightthickness=1,
                           highlightbackground='#c0c0c0')
            return ent

    def focus_next_field(self, idx):
        next_idx = (idx + 1) % len(self.tab_widgets)
        w = self.tab_widgets[next_idx]
        w.focus_set()
        if isinstance(w, tk.Text):
            w.mark_set("insert", "end")

    def build_address_list(self, parent):
        right_frame = tk.Frame(parent, bg='white')
        right_frame.grid(row=0, column=1, sticky='nsew', padx=10)
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(0, weight=1)

        canvas = tk.Canvas(right_frame,
                           bg='white',
                           highlightthickness=0)
        vscroll = ttk.Scrollbar(right_frame,
                                orient='vertical',
                                command=canvas.yview)

        self.entries_frame = tk.Frame(canvas, bg='white')

        self.entries_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.entries_frame, anchor="nw")

        canvas.configure(yscrollcommand=vscroll.set)

        canvas.grid(row=0, column=0, sticky="nsew")
        vscroll.grid(row=0, column=1, sticky="ns")

        self.refresh_entries()

    def refresh_entries(self):
        for w in self.entries_frame.winfo_children():
            w.destroy()

        addresses = read_csv(ADDRESS_FILE)

        for idx, entry in enumerate(addresses):
            self.render_entry(entry, idx)

    def render_entry(self, entry, idx):
        fr = tk.Frame(self.entries_frame,
                      bg="#e6f2ff",
                      bd=1,
                      relief='ridge')
        fr.pack(fill='x', pady=4)

        text = '\n'.join(f"{k}: {entry[k]}" for k in ADDRESS_FIELDS)
        lbl = tk.Label(fr,
                       text=text,
                       font=FONT_LABEL,
                       bg="#e6f2ff",
                       justify='left')
        lbl.pack(side='left', padx=8, pady=8, fill='x', expand=True)

        btn_frame = tk.Frame(fr, bg="#e6f2ff")
        btn_frame.pack(side="right", padx=8, pady=8)

        btn_edit = tk.Button(btn_frame,
                             text="Edit",
                             fg='white',
                             bg=PRIMARY_COLOR,
                             font=FONT_BTN,
                             relief='flat',
                             command=lambda i=idx: self.edit_entry(i))
        btn_edit.pack(side='left', padx=4)

        btn_print = tk.Button(btn_frame,
                              text="Print",
                              fg='white',
                              bg='#7B1FA2',
                              font=FONT_BTN,
                              relief='flat',
                              command=lambda e=entry: show_print([e]))
        btn_print.pack(side='left', padx=4)

        btn_delete = tk.Button(btn_frame,
                               text="Delete",
                               fg='white',
                               bg=DANGER_COLOR,
                               font=FONT_BTN,
                               relief='flat',
                               command=lambda i=idx: self.delete_entry(i))
        btn_delete.pack(side='left', padx=4)

    def save_entry(self):
        if not self.user:
            messagebox.showwarning("Access Denied", "Please login first to add entries.", parent=self.root)
            return

        entry = {}
        for k, w in self.widgets.items():
            if k == "Address":
                val = w.get("1.0", "end").strip()
            else:
                val = w.get().strip()
            entry[k] = val

        if any(not v for v in entry.values()):
            messagebox.showerror("Error", "All fields are required.", parent=self.root)
            return

        addresses = read_csv(ADDRESS_FILE)
        addresses.append(entry)
        write_csv(ADDRESS_FILE, addresses, ADDRESS_FIELDS)

        self.clear_form()
        self.refresh_entries()
        messagebox.showinfo("Success", "Entry saved.", parent=self.root)

    def clear_form(self):
        for k, w in self.widgets.items():
            if k == "Address":
                w.delete("1.0", "end")
            else:
                w.delete(0, "end")

    def edit_entry(self, idx):
        addresses = read_csv(ADDRESS_FILE)
        edit_data = addresses[idx]

        win = tk.Toplevel(self.root)
        win.title("Edit Entry")
        win.geometry("450x650")
        win.configure(bg='white')

        entry_widgets = {}

        for i, field in enumerate(ADDRESS_FIELDS):
            tk.Label(win, text=field + ":", bg='white', font=FONT_LABEL).grid(row=i, column=0, sticky='w', padx=10, pady=5)

            if field == "Address":
                txt = tk.Text(win,
                              width=30,
                              height=3,
                              font=FONT_LABEL,
                              bg=ENTRY_BG,
                              relief='flat',
                              highlightbackground='#c0c0c0',
                              highlightthickness=1)
                txt.insert('1.0', edit_data[field])
                txt.grid(row=i, column=1, padx=10, pady=5, sticky='ew')
                entry_widgets[field] = txt
            elif field == "State":
                combo = ttk.Combobox(win,
                                     values=INDIAN_STATES,
                                     font=FONT_LABEL,
                                     width=25)
                combo.set(edit_data[field])
                combo.grid(row=i, column=1, padx=10, pady=5, sticky='ew')
                entry_widgets[field] = combo
            elif field == "Country":
                combo = ttk.Combobox(win,
                                     values=COUNTRIES,
                                     font=FONT_LABEL,
                                     width=25)
                combo.set(edit_data[field])
                combo.grid(row=i, column=1, padx=10, pady=5, sticky='ew')
                entry_widgets[field] = combo
            elif field == "Type":
                combo = ttk.Combobox(win,
                                     values=["Personal", "Business"],
                                     font=FONT_LABEL,
                                     width=25)
                combo.set(edit_data[field])
                combo.grid(row=i, column=1, padx=10, pady=5, sticky='ew')
                entry_widgets[field] = combo
            else:
                ent = tk.Entry(win,
                               font=FONT_LABEL,
                               bg=ENTRY_BG,
                               relief='flat',
                               highlightbackground='#c0c0c0',
                               highlightthickness=1,
                               width=32)
                ent.insert(0, edit_data[field])
                ent.grid(row=i, column=1, padx=10, pady=5, sticky='ew')
                entry_widgets[field] = ent

        def save_changes():
            updated_entry = {}
            for field, widget in entry_widgets.items():
                if field == "Address":
                    val = widget.get("1.0", "end").strip()
                else:
                    val = widget.get().strip()
                if not val:
                    messagebox.showerror("Error", f"Field '{field}' is required.", parent=win)
                    return
                updated_entry[field] = val

            addresses[idx] = updated_entry
            write_csv(ADDRESS_FILE, addresses, ADDRESS_FIELDS)
            self.refresh_entries()

            messagebox.showinfo("Success", "Entry updated.", parent=win)
            win.destroy()  # Close the edit window

        save_btn = tk.Button(win,
                             text="Save Changes",
                             font=FONT_BTN,
                             bg=SUCCESS_COLOR,
                             fg='white',
                             relief='flat',
                             command=save_changes)
        save_btn.grid(row=len(ADDRESS_FIELDS), column=0, columnspan=2, pady=15, padx=10, sticky='ew')

    def delete_entry(self, idx):
        if messagebox.askyesno("Confirm", "Move this entry to Recycle Bin?", parent=self.root):
            addresses = read_csv(ADDRESS_FILE)
            recycle = read_csv(RECYCLE_FILE)
            recycle.append(addresses.pop(idx))
            write_csv(ADDRESS_FILE, addresses, ADDRESS_FIELDS)
            write_csv(RECYCLE_FILE, recycle, ADDRESS_FIELDS)
            self.refresh_entries()

    def delete_all_entries(self):
        if messagebox.askyesno("Confirm", "Move all entries to Recycle Bin?", parent=self.root):
            addresses = read_csv(ADDRESS_FILE)
            recycle = read_csv(RECYCLE_FILE)
            recycle.extend(addresses)
            write_csv(ADDRESS_FILE, [], ADDRESS_FIELDS)
            write_csv(RECYCLE_FILE, recycle, ADDRESS_FIELDS)
            self.refresh_entries()

    # --- Recycle Bin Operations ---

    def open_recycle_bin(self):
        if self.recycle_window is not None:
            self.recycle_window.lift()
            return

        self.recycle_window = tk.Toplevel(self.root)
        self.recycle_window.title("Recycle Bin")
        self.recycle_window.geometry("920x620")
        self.recycle_window.configure(bg='white')
        self.recycle_window.protocol("WM_DELETE_WINDOW", self._on_recycle_close)

        top_frame = tk.Frame(self.recycle_window, bg='white')
        top_frame.pack(fill='x', padx=10, pady=6)

        ttk.Button(top_frame, text="Recover All", style="Accent.TButton", command=self._recover_all).pack(side='left', padx=8)
        ttk.Button(top_frame, text="Delete All Permanently", command=self._delete_all_permanent).pack(side='left', padx=8)

        list_frame = tk.Frame(self.recycle_window, bg='white')
        list_frame.pack(fill='both', expand=True, padx=10, pady=6)

        canvas = tk.Canvas(list_frame, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=canvas.yview)

        self.recycle_entries_frame = tk.Frame(canvas, bg='white')
        self.recycle_entries_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window((0, 0), window=self.recycle_entries_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        self._populate_recycle_entries()

    def _populate_recycle_entries(self):
        for w in self.recycle_entries_frame.winfo_children():
            w.destroy()

        recycle_items = read_csv(RECYCLE_FILE)
        if not recycle_items:
            lbl = tk.Label(self.recycle_entries_frame, text="Recycle Bin is Empty", font=FONT_TITLE, bg='white')
            lbl.pack(pady=20)
            return

        for idx, entry in enumerate(recycle_items):
            frame = tk.Frame(self.recycle_entries_frame, bg=RECYCLE_BG, bd=1, relief='ridge')
            frame.pack(fill='x', pady=5, padx=5)

            text = "\n".join(f"{k}: {v}" for k, v in entry.items())
            lbl = tk.Label(frame, text=text, font=FONT_LABEL, bg=RECYCLE_BG, justify='left')
            lbl.pack(side='left', padx=8, pady=6, fill='both', expand=True)

            buttons_frame = tk.Frame(frame, bg=RECYCLE_BG)
            buttons_frame.pack(side='right', padx=8, pady=6)

            btn_rec = tk.Button(buttons_frame, text="Recover", font=FONT_BTN, fg='white', bg=SUCCESS_COLOR,
                                relief='flat', command=lambda i=idx: self._recover_one(i))
            btn_del = tk.Button(buttons_frame, text="Delete", font=FONT_BTN, fg='white', bg=DANGER_COLOR,
                                relief='flat', command=lambda i=idx: self._delete_one(i))

            btn_rec.pack(side='left', padx=4)
            btn_del.pack(side='left', padx=4)

    def _recover_one(self, index):
        recycle = read_csv(RECYCLE_FILE)
        if index >= len(recycle):
            return
        entry = recycle.pop(index)
        addresses = read_csv(ADDRESS_FILE)
        addresses.append(entry)
        write_csv(ADDRESS_FILE, addresses, ADDRESS_FIELDS)
        write_csv(RECYCLE_FILE, recycle, ADDRESS_FIELDS)
        messagebox.showinfo("Recovered", "Entry has been recovered.", parent=self.recycle_window)
        self._close_recycle_window()
        self.refresh_entries()

    def _delete_one(self, index):
        recycle = read_csv(RECYCLE_FILE)
        if index >= len(recycle):
            return
        answer = messagebox.askyesno("Confirm Delete", "Delete the selected entry permanently?", parent=self.recycle_window)
        if answer:
            recycle.pop(index)
            write_csv(RECYCLE_FILE, recycle, ADDRESS_FIELDS)
            messagebox.showinfo("Deleted", "Entry deleted permanently.", parent=self.recycle_window)
            self._close_recycle_window()

    def _recover_all(self):
        recycle = read_csv(RECYCLE_FILE)
        if not recycle:
            messagebox.showinfo("Empty", "Recycle bin is empty.", parent=self.recycle_window)
            return
        addresses = read_csv(ADDRESS_FILE)
        addresses.extend(recycle)
        write_csv(ADDRESS_FILE, addresses, ADDRESS_FIELDS)
        write_csv(RECYCLE_FILE, [], ADDRESS_FIELDS)
        messagebox.showinfo("Recovered", "All entries have been recovered.", parent=self.recycle_window)
        self._close_recycle_window()
        self.refresh_entries()

    def _delete_all_permanent(self):
        recycle = read_csv(RECYCLE_FILE)
        if not recycle:
            messagebox.showinfo("Empty", "Recycle bin is empty.", parent=self.recycle_window)
            return
        answer = messagebox.askyesno("Confirm Delete", "Delete all entries permanently?", parent=self.recycle_window)
        if answer:
            write_csv(RECYCLE_FILE, [], ADDRESS_FIELDS)
            messagebox.showinfo("Deleted", "All entries deleted permanently.", parent=self.recycle_window)
            self._close_recycle_window()

    def _close_recycle_window(self):
        if self.recycle_window is not None:
            self.recycle_window.destroy()
            self.recycle_window = None

    def _on_recycle_close(self):
        self.recycle_window = None
        self.recycle_window.destroy()


if __name__ == "__main__":
    # Ensure data folder and files exist
    for filepath, fields in [(USER_FILE, USER_FIELDS), (ADDRESS_FILE, ADDRESS_FIELDS), (RECYCLE_FILE, ADDRESS_FIELDS)]:
        if not os.path.exists(filepath):
            write_csv(filepath, [], fields)

    root = tk.Tk()
    root.geometry("1230x740")
    root.title("Secure Address Book")
    app = AddressBookApp(root)
    root.mainloop()

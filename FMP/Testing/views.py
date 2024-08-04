from django.shortcuts import render,get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from .forms import UploadFileForm,LoginForm,FacultyUpdateForm,SearchForm
from django.contrib import messages
import psycopg2
import pandas as pd
from sqlalchemy import create_engine, text

from .models import Faculty,YourModel

def main_page(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']  
            print(username) 
            print(password)
            if not(username) or not(password):
                messages.error(request,'These are required fields')

            # Your login logic here
            if username == 'Swathika' and password == 'swathi':
                # Successful login
                messages.success(request, 'Login successful')
            else:
                # Invalid login
                messages.error(request, 'Invalid username or password')
    else:
        form = LoginForm()

    return render(request, 'main_page.html', {'form': form})


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            print("yes")
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/success/')  # Redirect to success page
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form}) 



def handle_uploaded_file(file):
    import os
    upload_dir = 'UpFiles'
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    file_path = os.path.join(upload_dir, file.name)

    with open(file_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    Upload(file)
def Upload(file):
    import psycopg2
    import pandas as pd
    from sqlalchemy import create_engine, text

    # Define the database connection parameters
    db_params = {
        'host': '127.0.0.1',
        'database': 'postgres',
        'user': 'postgres',
        'password': 'crysis'
    }
    conn = psycopg2.connect(
        host=db_params['host'],
        database=db_params['database'],
        user=db_params['user'],
        password=db_params['password']
    )

    db_params['database'] = 'testing'
    engine = create_engine(f'postgresql://{db_params["user"]}:{db_params["password"]}@{db_params["host"]}/{db_params["database"]}')

    # Define the file paths for your CSV files
    csv_files = {
        'Faculty': "UpFiles/"+file.name
    }

    # Load and display the contents of each CSV file to check
    for table_name, file_path in csv_files.items():
        print(f"Contents of {table_name} CSV file:")
        df = pd.read_csv(file_path)
        print(df.head(2))  # Display the first few rows of the DataFrame
        print("\n")
    for table_name, file_path in csv_files.items():
        df = pd.read_csv(file_path)
        df.to_sql(table_name, engine, if_exists='replace', index=False)
def suc(request):
    return render(request,"Success.html")
def home(request):
    return render(request,"home.html")

def upload_detail(request):
    if request.method=='POST':
        name=request.POST.get('p_name')
        pan=request.POST.get('pan')
        qual=request.POST.get('qual')
        spec=request.POST.get('spec')
        des=request.POST.get('des')
        doj=request.POST.get('doj')
        dod=request.POST.get('dod')
        cur=request.POST.get('cur')
        asso=request.POST.get('as')
        con=request.POST.get('con')
        dol=request.POST.get('dol')
        db_params = {
        'host': '127.0.0.1',
        'database': 'testing',
        'user': 'postgres',
        'password': 'crysis'
        }
        conn = psycopg2.connect(
            host=db_params['host'],
            database=db_params['database'],
            user=db_params['user'],
            password=db_params['password']
        )

        # Create a cursor object
        cur = conn.cursor()
        print(f"jtffmh'{name}',{pan},''{qual}','{spec}','{des}','{doj}','{dod}','{cur}','{asso}','{con}','{dol}'")
        # Set automatic commit to be true, so that each action is committed without having to call conn.committ() after each command
        conn.set_session(autocommit=True)
        query=f"insert into Faculty values ('{name}',{pan},'{qual}','{spec}','{des}','{doj}','{dod}','{cur}','{asso}','{con}','{dol}');"
        cur.execute(query)
        conn.commit()
        cur.close()
        conn.close() 
        

    return render (request,"upload_one_data.html")

def search(request):
    selected_option = request.POST.get('selectOption', '') 
    # Define the database connection parameters
    db_params = {
        'host': '127.0.0.1',
        'database': 'testing',
        'user': 'postgres',
        'password': 'crysis'
    }
    conn = psycopg2.connect(
        host=db_params['host'],
        database=db_params['database'],
        user=db_params['user'],
        password=db_params['password']
    )

    # Create a cursor object
    cur = conn.cursor()

    # Set automatic commit to be true, so that each action is committed without having to call conn.committ() after each command
    conn.set_session(autocommit=True)

    # Create the 'soccer' database
    query = 'SELECT * FROM Faculty;'
    cur.execute(query)

    # Fetch all the rows from the result set
    rows = cur.fetchall()
    f=[]
    # Process the retrieved data (print in this example)
    for row in rows:
        f.append(list(row))
    # Commit the changes and close the connection to the default database
    conn.commit()
    cur.close()
    conn.close() 
    columns =['S.NO','Name','PAN No.',	'Qualification',	'Specialization',	'designation',	'DOJ'	,'Date_of_designation',	'Currently',	'Nature_of_Association'	,'If_contractual',	'Date_Leaving']
    return render(request,"faculty_search.html",{'data':f,'columns':columns})

def ma(request):
    return render(request,"main_page.html")

def faculty(request):
    return render(request,"faculty.html") 

def delete(request):  
    db_params = {
    'host': '127.0.0.1',
    'database': 'testing',
    'user': 'postgres',
    'password': 'crysis'
}
    conn = psycopg2.connect(
        host=db_params['host'],
        database=db_params['database'],
        user=db_params['user'],
        password=db_params['password']
    )

# Create a cursor object
    cur = conn.cursor()

# Set automatic commit to be true, so that each action is committed without having to call conn.committ() after each command
    conn.set_session(autocommit=True) 
    
#     name_to_delete = request.POST.get('nam', '')

# # Create the 'soccer' database
#     query = f"DELETE FROM team WHERE name = {name_to_delete}"
#     cur.execute(query)
    query = "SELECT * FROM Faculty order by name;"
    cur.execute(query)

    # Fetch all the rows from the result set
    rows = cur.fetchall()
    f=[]
    # Process the retrieved data (print in this example)
    for row in rows:
        print(row)
        f.append(list(row))
    # Commit the changes and close the connection to the default database
    conn.commit()
    cur.close()
    conn.close() 
    columns =['Name','PAN No.',	'Qualification',	'Specialization',	'designation',	'DOJ'	,'Date_of_designation',	'Currently',	'Nature_of_Association'	,'If_contractual',	'Date_Leaving']
    return render(request,"delete.html",{'data':f,'columns':columns})

def delete_search_data(request):  
    print("Sdfvkjsnkvsdiub")
    id_=request.POST.get ("FacultyName")
    db_params = {
    'host': '127.0.0.1',
    'database': 'testing',
    'user': 'postgres',
    'password': 'crysis'
}
    conn = psycopg2.connect(
        host=db_params['host'],
        database=db_params['database'],
        user=db_params['user'],
        password=db_params['password']
    )

# Create a cursor object
    cur = conn.cursor()

# Set automatic commit to be true, so that each action is committed without having to call conn.committ() after each command
    conn.set_session(autocommit=True) 
    
#     name_to_delete = request.POST.get('nam', '')

# # Create the 'soccer' database
#     query = f"DELETE FROM team WHERE name = {name_to_delete}"
#     cur.execute(query)
    query = f"select * FROM Faculty where name='{id_}';"
    cur.execute(query)

    # Fetch all the rows from the result set
    rows = cur.fetchall()
    f=[]
    # Process the retrieved data (print in this example)
    for row in rows:
        f.append(list(row))
    # Commit the changes and close the connection to the default database
    conn.commit()
    cur.close()
    conn.close() 
    columns =['Name','PAN No.',	'Qualification',	'Specialization',	'designation',	'DOJ'	,'Date_of_designation',	'Currently',	'Nature_of_Association'	,'If_contractual',	'Date_Leaving']
    return render(request,"delete.html",{'data':f,'columns':columns})
        
def delete_data(request):
    
    
    db_params = {
    'host': '127.0.0.1',
    'database': 'testing',
    'user': 'postgres',
    'password': 'crysis'
}
    conn = psycopg2.connect(
        host=db_params['host'],
        database=db_params['database'],
        user=db_params['user'],
        password=db_params['password']
    )

# Create a cursor object
    cur = conn.cursor()

# Set automatic commit to be true, so that each action is committed without having to call conn.committ() after each command
    conn.set_session(autocommit=True) 
    
    name_to_delete = request.POST.get('nam', '')

# # Create the 'soccer' database
#     query = f"DELETE FROM team WHERE name = {name_to_delete}"
#     cur.execute(query)
    query = f"delete FROM Faculty where name='{name_to_delete}';"
    cur.execute(query)
    conn.commit()
    query = f"select * FROM Faculty ;"
    cur.execute(query)
    # Fetch all the rows from the result set
    rows = cur.fetchall()
    print("Second")
    f=[]
    # Process the retrieved data (print in this example)
    for row in rows:
        print(row)
        f.append(list(row))
    # Commit the changes and close the connection to the default database
    cur.close()
    conn.commit()
    conn.close() 
    columns =['Name','PAN No.',	'Qualification',	'Specialization',	'designation',	'DOJ'	,'Date_of_designation',	'Currently',	'Nature_of_Association'	,'If_contractual',	'Date_Leaving']

    print(f)
    return render(request,"delete.html",{'data':f,'columns':columns})

    # return render(request,'delete.html')
def update_faculty(request, faculty_id):
    faculty = get_object_or_404(Faculty, pk=faculty_id)

    if request.method == 'POST':
        form = FacultyUpdateForm(request.POST, instance=faculty)
        if form.is_valid():
            form.save()
            return redirect('faculty_list')  # Redirect to a view displaying the list of faculty
    else:
        form = FacultyUpdateForm(instance=faculty)

    return render(request, 'update_faculty.html', {'form': form, 'faculty': faculty})

from django.shortcuts import render
import psycopg2

def search_view(request):
    if request.method == 'POST':
        selected_option = request.POST.get('selectOption', '')
        search_term = request.POST.get("FacultyName", '')

        db_params = {
            'host': '127.0.0.1',
            'database': 'testing',
            'user': 'postgres',
            'password': 'crysis'
        }

        # Use a context manager for the database connection
        with psycopg2.connect(
                host=db_params['host'],
                database=db_params['database'],
                user=db_params['user'],
                password=db_params['password']
        ) as conn:
            with conn.cursor() as cur:
                conn.set_session(autocommit=True)

                # Use parameterized queries to prevent SQL injection
                if selected_option == 'Name':
                    query = f"SELECT * FROM Faculty WHERE Name ='{search_term}';"
                elif selected_option == 'Designation':
                    query = f"SELECT * FROM Faculty WHERE designation='{search_term}';"
                elif selected_option == 'specialization':
                    query = f"SELECT * FROM Faculty WHERE specialization ='{search_term}';"

                cur.execute(query, (f'%{search_term}%',))

                # Fetch all the rows from the result set
                rows = cur.fetchall()
                data = [list(row) for row in rows]
                print(data)
        # Columns definition
        columns = ['S.NO','Name', 'PAN No.', 'Qualification', 'Specialization', 'designation', 'DOJ', 'Date_of_designation',
                   'Currently', 'Nature_of_Association', 'If_contractual', 'Date_Leaving']

        print(data, columns)
        return render(request, 'faculty_search.html', {'data': data, 'columns': columns})
    else:
        return render(request, 'faculty_search.html')



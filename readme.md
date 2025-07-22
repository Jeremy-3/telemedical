# 🩺 TeleMedical App – Setup Guide
*This is a simple Flask-based healthcare portal where users can register, log in, and interact with healthcare services. Admins can view, manage, and ban/unban users.*

## SET-UP

- Ensure you have the Following
    - Python(version 8) or higher
    - Any Browser compatible with `html` ,`css` and `javascript`


- Clone repository and open the folder:

        git clone git@github.com:Jeremy-3/telemedical.git
        cd telemedical


- Run the following command to install the dependencies from `Pipfile`:
        
         pipenv install

- Next enter the projects environment:

        pipenv shell

- Then run the following:

        flask db init      # Only once, if not already initialized
        flask db migrate
        flask db upgrade

- Run the `seed file` to populate the database:

        python seed.py

- Then run the application

        python main.py

- Locate the templates folder and open the file called `landingPage.html` .Open using a Browser and sing up or login to use the platform.


> [!NOTE]
> If you have more Suggestions, Do try and reach out . 

# Contributions 👥

<a name="cls"></a>

- Fork repository.

- Create a new Branch (`git checkout -b feature/your-branch-name`)

- Commit your changes(`git commit -m 'added some features`)

- Push to the Branch(`git push feature/your-branch-name`)

- Open a Pull Request

# 📄 lisenses

<a name="cls"></a>

This project is licensed under the MIT License . See the [LICENSE](https://opensource.org/license/mit) file for details.
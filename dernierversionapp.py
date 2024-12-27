import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
import hashlib

hide_warning_style = """
    <style>
    .stAlert {
        display: none;
    }
    </style>
    """
st.markdown(hide_warning_style, unsafe_allow_html=True)

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to load user credentials
def load_users():
    try:
        users = pd.read_csv('users.csv')
    except FileNotFoundError:
        users = pd.DataFrame(columns=['username', 'password'])
    return users

# Function to save user credentials
def save_user(username, password):
    users = load_users()
    hashed_password = hash_password(password)
    new_user = pd.DataFrame([[username, hashed_password]], columns=['username', 'password'])
    users = pd.concat([users, new_user], ignore_index=True)
    users.to_csv('users.csv', index=False)

# Function to check user credentials
def check_credentials(username, password):
    users = load_users()
    hashed_password = hash_password(password)
    user = users[(users['username'] == username) & (users['password'] == hashed_password)]
    return not user.empty

# Load and prepare data
data_path = '/Users/hadil/Desktop/monpfe hadil/base_de_donnees_tunisiennes.csv'  # Replace with your actual file path
data = pd.read_csv(data_path)

# Replace categorical values with numerical values
data['Sexe'] = data['Sexe'].map({'Homme': 0, 'Femme': 1})
data['Statut de fumeur'] = data['Statut de fumeur'].map({'Non': 0, 'Oui': 1})
data = pd.get_dummies(data, columns=['Region'])

# Define explanatory variables and target variable
X = data.drop(['Nom', 'Prenom', 'Prime d’assurance'], axis=1)
y = data['Prime d’assurance']

# Save the feature names
feature_names = X.columns

# Impute missing values
imputer = SimpleImputer(strategy='mean')
X_imputed = imputer.fit_transform(X)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_imputed, y, test_size=0.2, random_state=42)

# Normalize the data
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Define and train the linear regression model
model = LinearRegression()
model.fit(X_train_scaled, y_train)

# Function to predict insurance premium
def predict_premium(age, poids, sexe, statut_fumeur, region, nombre_enfants):
    user_data = pd.DataFrame({
        'Age': [age],
        'Poids': [poids],
        'Sexe': [sexe],
        'Statut de fumeur': [statut_fumeur],
        'Nombre d’enfants': [nombre_enfants],
        'Region_Ariana': [1 if region == 'Ariana' else 0],
        'Region_Bizerte': [1 if region == 'Bizerte' else 0],
        'Region_Ettadhamen': [1 if region == 'Ettadhamen' else 0],
        'Region_Gabès': [1 if region == 'Gabès' else 0],
        'Region_Autre': [1 if region == 'Autre' else 0]
    })
    
    # Align the columns with the training data
    user_data = user_data.reindex(columns=feature_names, fill_value=0)
    
    user_data_imputed = imputer.transform(user_data)
    user_data_scaled = scaler.transform(user_data_imputed)
    prediction = model.predict(user_data_scaled)
    return prediction[0]



# Home page
def home():
    st.markdown("""
        <style>
            .home-title {
                font-size: 50px;
                color: red; /* Changement de couleur en rouge */
                text-align: center;
                margin-top: 20px;
            }
            .home-subtitle {
                font-size: 30px;
                color: black; /* Changement de couleur en rouge */
                text-align: center;
                margin-bottom: 40px;
            }
            .home-content {
                font-size: 20px;
                color: #333333;
                text-align: center;
                margin: 0 auto;
                width: 60%;
                line-height: 1.6;
            }
      .home-image {
                display: block;
                margin-left: auto;
                margin-right: auto;
                max-width: 100%; /* Ajuster la largeur maximale de l'image */
            }
        </style>
        <div class="home-title">Bienvenue chez Gat Assurances</div>
        <div class="home-subtitle">Votre partenaire de confiance pour une vie assurée</div>
    """, unsafe_allow_html=True)
    
   
    # Afficher l'image avec Streamlit avec style inline
#st.image("/Users/hadil/Desktop/monpfe hadil/Unknown.jpeg")

    st.markdown("""
        <div class="home-content">
             Nous sommes ravis de vous accueillir sur notre plateforme. Gat Assurances est dédié à vous offrir les meilleures solutions d'assurance adaptées à vos besoins.
            Utilisez notre plateforme pour prédire la prime d'assurance et trouver la couverture qui vous convient le mieux. Explorez nos services et découvrez comment nous pouvons vous aider à protéger votre avenir.
        </div>
    """, unsafe_allow_html=True)
# Sign up page
def signup():
    st.markdown("""
        <style>
            .signup-title {
                font-size: 40px;
                color: #004080;
                text-align: center;
                margin-top: 20px;
            }
            .signup-form {
                font-size: 20px;
                color: #333333;
                width: 60%;
                margin: 0 auto;
                margin-top: 20px;
                line-height: 1.6;
            }
        </style>
        <div class="signup-title">Inscription</div>
    """, unsafe_allow_html=True)
    username = st.text_input("Nom d'utilisateur", key="signup_username")
    password = st.text_input("Mot de passe", type="password", key="signup_password")
    if st.button("S'inscrire"):
        users = load_users()
        if username in users['username'].values:
            st.warning("Nom d'utilisateur déjà utilisé. Veuillez en choisir un autre.")
        else:
            save_user(username, password)
            st.success("Inscription réussie. Vous pouvez maintenant vous connecter.")
            st.session_state.page = 'Connexion'  # Redirection vers la page de connexion
            st.experimental_set_query_params(page='Connexion')
            st.experimental_rerun()


# Function to check if user credentials are valid
def check_credentials(username, password):
    try:
        users = pd.read_csv('users.csv')
        user_row = users[(users['username'] == username) & (users['password'] == password)]
        return not user_row.empty
    except FileNotFoundError:
        return False

# Login page
def login():
    st.markdown("""
        <style>
            .login-title {
                font-size: 40px;
                color: #004080;
                text-align: center;
                margin-top: 20px;
            }
            .login-form {
                font-size: 20px;
                color: #333333;
                width: 60%;
                margin: 0 auto;
                margin-top: 20px;
                line-height: 1.6;
            }
        </style>
        <div class="login-title">Connexion</div>
    """, unsafe_allow_html=True)
    
    username = st.text_input("Nom d'utilisateur", key="login_username")
    password = st.text_input("Mot de passe", type="password", key="login_password")
    
    if st.button("Se connecter"):
        users = load_users()
        if username not in users['username'].values:
            st.error("Vous devez d'abord vous inscrire.")
        else:
            hashed_password = hash_password(password)
            if not check_credentials(username, hashed_password):
                st.error("Nom d'utilisateur ou mot de passe incorrect.")
            else:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.page = 'Prédiction'
                st.experimental_set_query_params(page='Prédiction')
                st.experimental_rerun()

# Function to check user credentials
def check_credentials(username, hashed_password):
    users = load_users()
    user = users[(users['username'] == username) & (users['password'] == hashed_password)]
    return not user.empty


# Prediction page
def prediction():
    st.markdown("""
        <style>
            .prediction-title {
                font-size: 40px;
                color: #004080;
                text-align: center;
                margin-top: 20px;
            }
            .prediction-form {
                font-size: 20px;
                color: #333333;
                width: 60%;
                margin: 0 auto;
                margin-top: 20px;
                line-height: 1.6;
            }
        </style>
        <div class="prediction-title">Prédiction des Primes d'Assurance</div>
    """, unsafe_allow_html=True)
    age = st.number_input("Âge", min_value=18, max_value=100, value=30)
    poids = st.number_input("Poids (kg)", min_value=30.0, max_value=200.0, value=70.0)
    sexe = st.selectbox("Sexe", ["Homme", "Femme"])
    statut_fumeur = st.selectbox("Statut de fumeur", ["Non", "Oui"])
    region = st.selectbox("Région", ["Gabès", "Ettadhamen", "Ariana", "Bizerte", "Autre"])
    nombre_enfants = st.number_input("Nombre d’enfants", min_value=0, max_value=10, value=0)

    sexe_val = 0 if sexe == 'Homme' else 1
    statut_fumeur_val = 0 if statut_fumeur == 'Non' else 1

    if st.button("Prédire"):
        prediction = predict_premium(age, poids, sexe_val, statut_fumeur_val, region, nombre_enfants)
        st.write(f"La prime d'assurance estimée est de {prediction:.2f} Dinars.")

# Contact page
def contact():
    st.markdown("""
        <style>
            .contact-title {
                font-size: 40px;
                color: #004080;
                text-align: center;
                margin-top: 20px;
            }
            .contact-content {
                font-size: 20px;
                color: #333333;
                width: 60%;
                margin: 0 auto;
                margin-top: 20px;
                line-height: 1.6;
                text-align: center;
            }
            .social-icons {
                display: flex;
                justify-content: center;
                margin-top: 20px;
            }
            .social-icon {
                margin: 0 10px;
            }
            .social-icon img {
                width: 40px;
                height: 40px;
            }
        </style>
        <div class="contact-title">Contactez-nous</div>
        <div class="contact-content">
            Si vous avez des questions ou avez besoin de plus d'informations, n'hésitez pas à nous contacter.
            <br><br>
            - **Téléphone:** +216 123 456 789
            <br>
            - **Email:** contact@gatassurances.tn
            <br>
            - **Adresse:** 123 Avenue de l'Assurance, Tunis, Tunisie
            <br><br>
            <div class="social-icons">
                <a href="https://www.facebook.com/GATASSURANCESTN/?locale=fr_FR" class="social-icon"><img src="https://upload.wikimedia.org/wikipedia/commons/5/51/Facebook_f_logo_%282019%29.svg" alt="Facebook"></a>
                <a href="https://www.instagram.com/gatassurances/" class="social-icon"><img src="https://upload.wikimedia.org/wikipedia/commons/a/a5/Instagram_icon.png" alt="Instagram"></a>
                <a href="https://x.com/gatassurances" class="social-icon"><img src="https://upload.wikimedia.org/wikipedia/commons/6/6f/Logo_of_Twitter.svg" alt="Twitter"></a>
            </div>
        </div>
    """, unsafe_allow_html=True)

# Main application
def main():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'page' not in st.session_state:
        st.session_state.page = 'Accueil'

    # Top menu
    menu = ["Accueil", "Contact", "Inscription", "Connexion", "Prédiction"]
    menu_actions = {
        "Accueil": home,
        "Contact": contact,
        "Inscription": signup,
        "Connexion": login,
        "Prédiction": prediction
    }
    
    st.markdown("""
        <style>
        .menu-container {
            display: flex;
            justify-content: space-around;
            background-color: #f4f4f4;
            padding: 10px 0;
            margin-bottom: 20px;
        }
        .menu-item {
            flex: 1;
            text-align: center;
            font-size: 20px;
        }
        .menu-item a {
            text-decoration: none;
            color: black;
            padding: 10px;
            display: block;
        }
        .menu-item a:hover {
            background-color: #ddd;
        }
        </style>
    """, unsafe_allow_html=True)

    menu_html = '<div class="menu-container">' + ''.join(
        [f'<div class="menu-item"><a href="?page={item}">{item}</a></div>' for item in menu]
    ) + '</div>'

    st.markdown(menu_html, unsafe_allow_html=True)

    # Page navigation
    query_params = st.experimental_get_query_params()
    if 'page' in query_params:
        st.session_state.page = query_params['page'][0]

    if st.session_state.logged_in and st.session_state.page == 'Connexion':
        st.session_state.page = 'Prédiction'
        st.experimental_set_query_params(page='Prédiction')
        st.experimental_rerun()

    page = st.session_state.page

    if page in menu_actions:
        menu_actions[page]()
    else:
        home()

if __name__ == '__main__':
    main()
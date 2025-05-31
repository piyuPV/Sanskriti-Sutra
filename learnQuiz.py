import streamlit as st
import time
import random

def learnQuiz():
    # Initialize session state for quiz
    if 'quiz_started' not in st.session_state:
        st.session_state.quiz_started = False
    if 'answers' not in st.session_state:
        st.session_state.answers = {}
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'time_left' not in st.session_state:
        st.session_state.time_left = 60
    if 'submitted' not in st.session_state:
        st.session_state.submitted = False

    st.title("Learn & Quiz - Indian Cultural Heritage")
    
    # Cultural topics and their content
    topics = {
    "Monuments": {
        "Taj Mahal": {
            "image": "assets/learning/tajmahal.jpg",
            "description": """
            The Taj Mahal is an ivory-white marble mausoleum on the right bank of the river Yamuna in Agra, India.\n
            • Built between 1632-1648 by Mughal Emperor Shah Jahan as a symbol of love for his wife Mumtaz Mahal.\n
            • UNESCO World Heritage Site and one of the New Seven Wonders of the World.\n
            • Exemplifies Mughal architecture, blending Persian, Islamic, and Indian styles.\n
            • Renowned for its symmetrical gardens, intricate marble inlay work, and the iconic central dome.\n
            • The monument attracts millions of visitors annually and is a global symbol of India’s rich heritage.\n
            """
        },
        "Red Fort": {
            "image": "assets/learning/redfort.jpg",
            "description": """
            The Red Fort is a historic fortress built in the 17th century located in Delhi, India.\n
            • Constructed by Mughal Emperor Shah Jahan in 1639 when he shifted his capital from Agra to Delhi.\n
            • Served as the main residence of Mughal Emperors for nearly 200 years.\n
            • Made of striking red sandstone, featuring massive walls, ornate gates, and beautiful gardens.\n
            • Houses several museums and is a center for cultural and national events, including India's Independence Day celebrations.\n
            • UNESCO World Heritage Site, representing the zenith of Mughal creativity under Shah Jahan.\n
            """
        },
        "Qutub Minar": {
            "image": "assets/learning/qutubminar.jpg",
            "description": """
            Qutub Minar is a soaring, 73-meter tall minaret in Delhi, India, and is the tallest brick minaret in the world.\n
            • Construction began in 1192 by Qutb-ud-din Aibak and was completed by his successors.\n
            • Built to celebrate Muslim dominance in Delhi after the defeat of Delhi's last Hindu ruler.\n
            • The tower is made of red sandstone and marble, adorned with intricate carvings and verses from the Quran.\n
            • The Qutub complex also includes ancient mosques, tombs, and the famous Iron Pillar of Delhi.\n
            • UNESCO World Heritage Site, it stands as a testament to early Indo-Islamic architecture and engineering.\n
            """
        },
        "Gateway of India": {
            "image": "assets/learning/gatewayofindia.jpg",
            "description": """
            The Gateway of India is a majestic arch-monument located on the waterfront in Mumbai, Maharashtra.\n
            • Built between 1913 and 1924 to commemorate the landing of King George V and Queen Mary in India in 1911.\n
            • Designed in the Indo-Saracenic architectural style, blending elements of Hindu and Muslim architectural forms.\n
            • The structure is 26 meters high and made of yellow basalt and reinforced concrete.\n
            • Historically, it served as the ceremonial entrance to India for Viceroys and new Governors of Bombay.\n
            • Today, it is a popular tourist destination and a symbol of Mumbai's cosmopolitan heritage.\n
            """
        },
        "Sun Temple, Konark": {
            "image": "assets/learning/suntemple.jpg",
            "description": """
            The Sun Temple at Konark is a 13th-century temple dedicated to the Hindu Sun God, Surya, located in Odisha.\n
            • Built by King Narasimhadeva I of the Eastern Ganga dynasty in 1250 CE.\n
            • Designed in the shape of a colossal chariot with intricately carved stone wheels, pillars, and walls.\n
            • Famous for its exquisite stone carvings depicting deities, dancers, musicians, and scenes from daily life.\n
            • UNESCO World Heritage Site and one of the finest examples of Kalinga architecture.\n
            • The temple is renowned for its alignment with the sunrise and its annual Konark Dance Festival, celebrating classical Indian dance.\n
            """
        }
    },
    "Art Forms": {
        "Bharatanatyam": {
            "image": "assets/learning/bharatanatyam.jpg",
            "description": """
            Bharatanatyam is a major form of Indian classical dance originating from Tamil Nadu.\n
            • One of the oldest classical dance traditions in India, with origins dating back over 2000 years.\n
            • Known for its grace, purity, tenderness, and sculpturesque poses inspired by temple art.\n
            • Features expressive hand gestures (mudras), intricate footwork, and elaborate costumes.\n
            • Traditionally performed by women in temples as a form of worship and storytelling.\n
            • Today, it is performed on stages worldwide, symbolizing South Indian cultural heritage.\n
            """
        },
        "Kathakali": {
            "image": "assets/learning/kathakali.jpg",
            "description": """
            Kathakali is a major form of classical Indian dance from Kerala.\n
            • Renowned for its colorful and elaborate costumes, towering headgear, and painted faces.\n
            • Performances are based on stories from Indian epics like the Mahabharata and Ramayana.\n
            • Combines dance, drama, music, and ritual, with highly stylized movements and facial expressions.\n
            • Traditionally performed by male artists, often lasting through the night.\n
            • Recognized globally for its unique visual spectacle and storytelling tradition.\n
            """
        },
        "Odissi": {
            "image": "assets/learning/odissi.jpg",
            "description": """
            Odissi is a classical dance form from Odisha, India.\n
            • Characterized by fluid movements, sculpturesque poses, and expressive gestures.\n
            • Originated in ancient Hindu temples as a form of devotion and storytelling.\n
            • Dancers wear silver jewelry and traditional costumes, performing to Odissi music.\n
            • Themes often depict stories of Lord Jagannath, Krishna, and episodes from mythology.\n
            • Recognized as one of the eight classical dance forms of India, celebrated for its lyrical beauty.\n
            """
        },
        "Madhubani Painting": {
            "image": "assets/learning/madhubani.jpg",
            "description": """
            Madhubani painting is a traditional folk art from the Mithila region of Bihar.\n
            • Known for its vibrant colors, geometric patterns, and depiction of nature and mythology.\n
            • Traditionally painted on walls and floors during festivals and special occasions.\n
            • Uses natural dyes and pigments, applied with fingers, twigs, or brushes.\n
            • Common themes include Hindu deities, flora, fauna, and scenes of village life.\n
            • Recognized globally for its intricate designs and cultural significance.\n
            """
        },
        "Dhokra Art": {
            "image": "assets/learning/dhokra.jpg",
            "description": """
            Dhokra art is an ancient form of metal casting practiced by tribal communities in central and eastern India.\n
            • Uses the lost-wax casting technique, dating back over 4000 years.\n
            • Artisans create intricate figurines, animals, and ritual objects from brass and bronze.\n
            • Designs often feature motifs from nature, mythology, and tribal folklore.\n
            • Dhokra products are prized for their rustic charm and artistic value.\n
            • This craft supports the livelihoods of many artisan families in states like Chhattisgarh, Odisha, and West Bengal.\n
            """
        }
    },
    "Festivals": {
        "Diwali": {
            "image": "assets/learning/diwali.jpg",
            "description": """
            Diwali is the festival of lights celebrated across India.\n
            • Five-day festival symbolizing the victory of light over darkness and good over evil.\n
            • Celebrated with oil lamps (diyas), fireworks, sweets, and family gatherings.\n
            • Associated with the return of Lord Rama to Ayodhya after defeating Ravana, as per the Ramayana.\n
            • Houses and streets are decorated with colorful rangoli and lights.\n
            • Observed by Hindus, Jains, Sikhs, and Buddhists, making it one of India's most inclusive festivals.\n
            """
        },
        "Holi": {
            "image": "assets/learning/holi.jpg",
            "description": """
            Holi is the festival of colors celebrated in spring.\n
            • Marks the arrival of spring and the end of winter.\n
            • Known for playful throwing of colored powders and water among friends and family.\n
            • Symbolizes the victory of good over evil, commemorating the legend of Prahlad and Holika.\n
            • Celebrated with music, dance, sweets, and festive foods like gujiya and thandai.\n
            • Brings communities together in a joyful and vibrant atmosphere.\n
            """
        },
        "Durga Puja": {
            "image": "assets/learning/durgapuja.jpg",
            "description": """
            Durga Puja is a major Hindu festival celebrated primarily in West Bengal, Assam, and other eastern states.\n
            • Honors the goddess Durga’s victory over the buffalo demon Mahishasura.\n
            • Celebrated with elaborate clay idols, artistic pandals (temporary structures), and cultural performances.\n
            • Involves rituals, prayers, processions, and immersion of idols in rivers.\n
            • Marks a time for family reunions, feasting, and wearing new clothes.\n
            • Recognized as an Intangible Cultural Heritage by UNESCO for its artistic and cultural significance.\n
            """
        },
        "Pongal": {
            "image": "assets/learning/pongal.jpg",
            "description": """
            Pongal is a harvest festival celebrated mainly in Tamil Nadu.\n
            • Marks the beginning of the sun’s northward journey (Uttarayan) and the end of the winter solstice.\n
            • Celebrated over four days with rituals, traditional music, and dance.\n
            • Special dish called 'Pongal' is prepared by boiling rice with milk and jaggery.\n
            • Farmers thank the Sun God and cattle for a bountiful harvest.\n
            • Symbolizes prosperity, gratitude, and the joy of rural life.\n
            """
        },
        "Eid-ul-Fitr": {
            "image": "assets/learning/eid.jpg",
            "description": """
            Eid-ul-Fitr is an important Islamic festival marking the end of Ramadan, the holy month of fasting.\n
            • Celebrated with prayers, feasting, and giving of charity (Zakat al-Fitr).\n
            • Families and friends gather to share special dishes and sweets like seviyan and biryani.\n
            • New clothes are worn, and homes are decorated for the occasion.\n
            • Emphasizes forgiveness, gratitude, and community spirit.\n
            • One of the most significant festivals for Muslims in India and around the world.\n
            """
        }
    }
}

    # Quiz questions
    quiz_questions = {
    "Monuments": [
        {
            "question": "What is the unique feature of the Taj Mahal’s main dome?",
            "options": [
                "It is supported by iron beams",
                "It is self-supporting with no reinforcing struts or columns",
                "It is made of red sandstone",
                "It is octagonal in shape"
            ],
            "correct": "It is self-supporting with no reinforcing struts or columns"
        },
        {
            "question": "How many minarets surround the Taj Mahal and what was their original purpose?",
            "options": [
                "2, for decoration",
                "4, to call the faithful to prayer",
                "6, for symmetry",
                "8, for structural support"
            ],
            "correct": "4, to call the faithful to prayer"
        },
        {
            "question": "What is the name of the terrace that forms the riverfront of the Taj Mahal complex?",
            "options": [
                "Charbagh",
                "Chabutra",
                "Chhatri",
                "Guldasta"
            ],
            "correct": "Chabutra"
        },
        {
            "question": "Which precious technique is used for decorating the marble surfaces of the Taj Mahal?",
            "options": [
                "Fresco",
                "Pietra dura (stone inlay)",
                "Enamel painting",
                "Mosaic"
            ],
            "correct": "Pietra dura (stone inlay)"
        },
        {
            "question": "Where are the real graves of Mumtaz Mahal and Shah Jahan located in the Taj Mahal?",
            "options": [
                "In the main dome chamber",
                "In the lower tomb chamber (crypt)",
                "In the garden",
                "In the mosque"
            ],
            "correct": "In the lower tomb chamber (crypt)"
        },
        {
            "question": "Which architectural element is used to accentuate the height of the Taj Mahal’s main dome?",
            "options": [
                "Lotus design",
                "Peacock motif",
                "Sun dial",
                "Elephant carving"
            ],
            "correct": "Lotus design"
        },
        {
            "question": "What material is used for the mosque and guest house in the Taj Mahal complex?",
            "options": [
                "White marble",
                "Red sandstone",
                "Granite",
                "Limestone"
            ],
            "correct": "Red sandstone"
        },
        {
            "question": "What is the design of the Taj Mahal’s garden intended to symbolize?",
            "options": [
                "Royalty",
                "Paradise on Earth",
                "Victory in battle",
                "Unity in diversity"
            ],
            "correct": "Paradise on Earth"
        },
        {
            "question": "Which chief architect is credited with the design of the Taj Mahal?",
            "options": [
                "Ustad Ahmad Lahauri",
                "Mirza Ghalib",
                "Akbar the Great",
                "Sir Edwin Lutyens"
            ],
            "correct": "Ustad Ahmad Lahauri"
        },
        {
            "question": "What happens to the color of the Taj Mahal’s marble at different times of day?",
            "options": [
                "It remains always white",
                "It reflects different hues depending on sunlight or moonlight",
                "It turns red at sunset",
                "It glows in the dark"
            ],
            "correct": "It reflects different hues depending on sunlight or moonlight"
        }
    ],
    "Art Forms": [
        {
            "question": "Which classical dance form is known for its sculpturesque poses inspired by temple art?",
            "options": ["Kathakali", "Bharatanatyam", "Odissi", "Kuchipudi"],
            "correct": "Bharatanatyam"
        },
        {
            "question": "Kathakali performances are traditionally based on stories from which Indian epics?",
            "options": ["Mahabharata and Ramayana", "Vedas", "Upanishads", "Puranas"],
            "correct": "Mahabharata and Ramayana"
        },
        {
            "question": "Which folk art from Bihar uses natural dyes and is known for geometric patterns and depiction of nature?",
            "options": ["Warli", "Madhubani", "Pattachitra", "Gond"],
            "correct": "Madhubani"
        },
        {
            "question": "Dhokra art uses which ancient technique for metal casting?",
            "options": ["Sand casting", "Lost-wax casting", "Die casting", "Clay casting"],
            "correct": "Lost-wax casting"
        },
        {
            "question": "Odissi dance is traditionally performed to music in which language?",
            "options": ["Hindi", "Sanskrit", "Odia", "Bengali"],
            "correct": "Odia"
        },
        {
            "question": "Which dance form originated as a temple dance performed by women as a form of worship and storytelling?",
            "options": ["Kathak", "Bharatanatyam", "Sattriya", "Manipuri"],
            "correct": "Bharatanatyam"
        },
        {
            "question": "What is a distinctive feature of Kathakali costumes?",
            "options": [
                "Minimalist attire",
                "Colorful, elaborate costumes and painted faces",
                "White sarees with gold borders",
                "Headgear with peacock feathers"
            ],
            "correct": "Colorful, elaborate costumes and painted faces"
        },
        {
            "question": "Which art form is practiced by tribal communities in Chhattisgarh, Odisha, and West Bengal?",
            "options": ["Dhokra", "Tanjore painting", "Phad", "Pattachitra"],
            "correct": "Dhokra"
        },
        {
            "question": "Madhubani painting is traditionally done on which surfaces during festivals?",
            "options": ["Paper", "Walls and floors", "Cloth", "Canvas"],
            "correct": "Walls and floors"
        },
        {
            "question": "Which classical dance form is celebrated for its lyrical beauty and depiction of stories of Lord Jagannath?",
            "options": ["Odissi", "Kuchipudi", "Mohiniyattam", "Kathak"],
            "correct": "Odissi"
        }
    ],
    "Festivals": [
        {
            "question": "How many days is Diwali celebrated?",
            "options": ["Three", "Four", "Five", "Seven"],
            "correct": "Five"
        },
        {
            "question": "When is Holi celebrated?",
            "options": ["Summer", "Winter", "Spring", "Autumn"],
            "correct": "Spring"
        },
        {
            "question": "Which festival marks the end of Ramadan and is celebrated with charity and feasting?",
            "options": ["Bakrid", "Eid-ul-Fitr", "Muharram", "Shab-e-Barat"],
            "correct": "Eid-ul-Fitr"
        },
        {
            "question": "Durga Puja is recognized by UNESCO as what type of heritage?",
            "options": [
                "World Heritage Site",
                "Intangible Cultural Heritage",
                "Natural Heritage",
                "Architectural Heritage"
            ],
            "correct": "Intangible Cultural Heritage"
        },
        {
            "question": "During Pongal, which special dish is traditionally prepared and offered to the Sun God?",
            "options": ["Payasam", "Pongal", "Ladoo", "Halwa"],
            "correct": "Pongal"
        },
        {
            "question": "Which festival is associated with the return of Lord Rama to Ayodhya?",
            "options": ["Diwali", "Holi", "Navratri", "Raksha Bandhan"],
            "correct": "Diwali"
        },
        {
            "question": "Holi commemorates the victory of Prahlad over which demoness?",
            "options": ["Holika", "Putana", "Surpanakha", "Trijata"],
            "correct": "Holika"
        },
        {
            "question": "Which festival is known for its elaborate clay idols and artistic pandals?",
            "options": ["Ganesh Chaturthi", "Durga Puja", "Janmashtami", "Onam"],
            "correct": "Durga Puja"
        },
        {
            "question": "Which harvest festival marks the beginning of the sun’s northward journey (Uttarayan) in Tamil Nadu?",
            "options": ["Pongal", "Baisakhi", "Makar Sankranti", "Lohri"],
            "correct": "Pongal"
        },
        {
            "question": "Which sweet dish is commonly prepared during Eid-ul-Fitr?",
            "options": ["Gujiya", "Seviyan", "Modak", "Rasgulla"],
            "correct": "Seviyan"
        }
    ]
}



    # Topic selection
    selected_topic = st.selectbox("Select a Topic to Learn:", list(topics.keys()))

    # Display content for selected topic
    if selected_topic:
        st.header(f"Learning about {selected_topic}")
        for item, content in topics[selected_topic].items():
            with st.expander(f"Learn about {item}"):
                try:
                    st.image(content["image"], caption=item)
                except:
                    st.error(f"Image not found for {item}")
                st.markdown(content["description"])

        # Start Quiz button
        if not st.session_state.quiz_started and st.button("Take Quiz"):
            st.session_state.quiz_started = True
            st.session_state.time_left = 60
            st.session_state.submitted = False
            st.session_state.score = 0
            # Randomly select and store questions
            questions = quiz_questions[selected_topic]
            random.shuffle(questions)
            st.session_state.current_questions = questions[:10]
            st.rerun()  # Changed from experimental_rerun to rerun

        # Quiz section
        if st.session_state.quiz_started:
            st.header("Quiz Time!")
            
            # Display timer
            st.write(f"Time remaining: {st.session_state.time_left} seconds")
            
            # Display questions
            for i, q in enumerate(st.session_state.current_questions):
                st.subheader(f"Q{i+1}: {q['question']}")
                st.session_state.answers[i] = st.radio(
                    "Select your answer:",
                    q['options'],
                    key=f"q_{i}",
                    disabled=st.session_state.submitted
                )

            # Submit button
            if not st.session_state.submitted and st.button("Submit Quiz"):
                st.session_state.submitted = True
                # Calculate score
                score = 0
                for i, q in enumerate(st.session_state.current_questions):
                    if st.session_state.answers.get(i) == q['correct']:
                        score += 1
                st.session_state.score = score
                
            # Display results if submitted
            if st.session_state.submitted:
                st.success(f"Quiz completed! Your score: {st.session_state.score}/10")
                if st.button("Take Another Quiz"):
                    st.session_state.quiz_started = False
                    st.session_state.submitted = False
                    st.rerun()  # Changed from experimental_rerun to rerun

            # Update timer
            if not st.session_state.submitted:
                time.sleep(1)
                st.session_state.time_left -= 1
                if st.session_state.time_left <= 0:
                    st.session_state.submitted = True
                    st.warning("Time's up!")
                    st.rerun()  # Changed from experimental_rerun to rerun

# Add custom styling
st.markdown("""
    <style>
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
    }
    .quiz-container {
        background-color: rgba(255,255,255,0.1);
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)
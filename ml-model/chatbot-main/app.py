from flask import Flask, render_template, request, jsonify
import json
import string
import random
import nltk
import numpy as np
from nltk.stem import WordNetLemmatizer
import tensorflow as tf
from tensorflow import keras
from keras import Sequential
from keras.layers import Dense, Dropout

nltk.download('punkt')
nltk.download('wordnet')

app = Flask(__name__)

# Data untuk pelatihan
ourData = {
    "intents": [
        {"tag": "sapaan", "patterns": ["Halo", "Hai", "Hai kamu"], "responses": ["Halo juga! Selamat datang di Peta Mimpi, aplikasi pribadi untuk menjelajahi dunia mimpi dan mengeksplorasi kepribadian Anda melalui MBTI."]},

        {"tag": "mbti_intro", "patterns": ["Apa itu MBTI?", "Bagaimana MBTI bekerja?"], "responses": ["MBTI (Myers-Briggs Type Indicator) adalah alat pengukur kepribadian yang membantu mengidentifikasi preferensi psikologis dalam empat dimensi: Ekstrovert (E) vs. Introvert (I), Sensorik (S) vs. Intuitif (N), Pemikiran (T) vs. Perasaan (F), dan Pengatur (J) vs. Perseptif (P). Aplikasi Peta Mimpi kami menggunakan MBTI untuk memberikan pengalaman unik dalam memahami dunia mimpi dan kepribadian Anda."]},

        {"tag": "tes_mbti", "patterns": ["Bagaimana cara melakukan tes MBTI?", "Tes kepribadian MBTI"], "responses": ["Tes MBTI di aplikasi Peta Mimpi kami dirancang untuk membantu Anda memahami preferensi kepribadian Anda. Jawablah serangkaian pertanyaan dengan jujur dan hasilnya akan memberikan wawasan yang mendalam tentang tipe kepribadian Anda."]},

        {"tag": "mimpi_malam_ini", "patterns": ["Apa arti mimpi malam ini?", "Bisakah kamu menafsirkan mimpi saya?"], "responses": ["Tentu, saya dapat membantu Anda menafsirkan mimpi Anda. Namun, hasil tafsiran akan lebih akurat jika Anda telah melakukan tes MBTI. Tes ini membantu mengaitkan mimpi Anda dengan preferensi kepribadian, memberikan pemahaman yang lebih dalam."]},

        {"tag": "temukan_mimpi", "patterns": ["Bagaimana cara menemukan mimpi yang bermakna?", "Berikan saran untuk menjelajahi mimpi"], "responses": ["Untuk menemukan mimpi yang bermakna, gunakan fitur pencarian di aplikasi Peta Mimpi berdasarkan tipe kepribadian MBTI Anda. Ini akan membimbing Anda ke dalam dunia mimpi yang paling sesuai dengan preferensi Anda, memberikan pengalaman menjelajah yang unik."]},

        {"tag": "simpan_mimpi", "patterns": ["Bagaimana cara menyimpan mimpi?", "Bisakah saya menyimpan mimpi favorit saya?"], "responses": ["Anda dapat menyimpan mimpi favorit Anda di aplikasi Peta Mimpi. Cukup pilih opsi 'Simpan' ketika Anda menemukan mimpi yang ingin Anda ingat. Ini memungkinkan Anda melacak dan merenungkan kembali pengalaman mimpi yang paling berkesan."]},

        {"tag": "eksplorasi_mbti", "patterns": ["Bagaimana cara menjelajahi dunia mimpi berdasarkan MBTI?", "Temukan mimpi berdasarkan tipe kepribadian"], "responses": ["Peta Mimpi kami menawarkan fitur eksplorasi berdasarkan tipe kepribadian MBTI. Setelah Anda menyelesaikan tes, masukkan tipe kepribadian Anda dan nikmati pengalaman eksplorasi mimpi yang sesuai dengan preferensi Anda."]},

        {"tag": "tipe_mbti", "patterns": ["Berikan contoh tipe kepribadian MBTI", "Apa saja jenis kepribadian MBTI?"], "responses": ["Contoh tipe kepribadian MBTI mencakup INTJ (Ilmiah), ENFP (Pencipta), ISFJ (Pelindung), dan ISTP (Ahli). Setiap tipe memiliki ciri-ciri unik, dan aplikasi Peta Mimpi akan membantu Anda menemukan mimpi yang cocok dengan kepribadian Anda."]},

        {"tag": "tanya_pribadi", "patterns": ["Beri saya pertanyaan uji kepribadian", "Tes kepribadian tambahan"], "responses": ["Tentu, berikut beberapa pertanyaan tambahan untuk merangsang refleksi diri Anda: 1. Apa yang membuat Anda merasa hidup? 2. Bagaimana cara Anda merespons situasi stres? 3. Pilih satu kata yang paling menggambarkan diri Anda."]},

        {"tag": "fitur_aplikasi", "patterns": ["Apa fitur-fitur utama Peta Mimpi?", "Apa yang bisa dilakukan aplikasi ini?"], "responses": ["Peta Mimpi memiliki empat fitur utama yang memungkinkan Anda menjelajahi dunia mimpi dan mengembangkan diri: 1. Personality Test: Temukan tipe kepribadian MBTI Anda. 2. Kenali Minat: Identifikasi minat dan passion Anda. 3. Kembangkan Bakat: Temukan potensi bakat dan kembangkan keterampilan unik Anda. 4. Rekomendasi Karir dan Jurusan: Dapatkan saran mengenai karir dan jurusan yang sesuai dengan kepribadian dan minat Anda."]},

        {"tag": "kenali_minat", "patterns": ["Bagaimana cara mengenali minat saya?", "Fitur Kenali Minat"], "responses": ["Fitur Kenali Minat di Peta Mimpi membantu Anda mengidentifikasi minat dan passion Anda. Jawablah serangkaian pertanyaan dan temukan area minat yang dapat menjadi panduan dalam pemilihan karir dan pengembangan diri Anda."]},

        {"tag": "kembangkan_bakat", "patterns": ["Bagaimana cara mengembangkan bakat saya?", "Fitur Kembangkan Bakat"], "responses": ["Fitur Kembangkan Bakat memberikan panduan langkah demi langkah untuk mengembangkan bakat dan keterampilan unik Anda. Temukan potensi terpendam dan dorong pertumbuhan diri Anda."]},

        {"tag": "rekomendasi_karir", "patterns": ["Bisakah saya mendapatkan rekomendasi karir?", "Fitur Rekomendasi Karir dan Jurusan"], "responses": ["Ya, tentu! Fitur Rekomendasi Karir dan Jurusan di Peta Mimpi memberikan saran berdasarkan tipe kepribadian, minat,"]}
    ]
}


# Tokenizer dan Lemmatizer
lm = WordNetLemmatizer()

# Mengumpulkan kata-kata dan kelas
ourClasses = []
newWords = []
documentX = []
documentY = []

for intent in ourData["intents"]:
    for pattern in intent["patterns"]:
        ourTokens = nltk.word_tokenize(pattern)
        newWords.extend(ourTokens)
        documentX.append(pattern)
        documentY.append(intent["tag"])

    if intent["tag"] not in ourClasses:
        ourClasses.append(intent["tag"])

newWords = [lm.lemmatize(word.lower()) for word in newWords if word not in string.punctuation]
newWords = sorted(set(newWords))
ourClasses = sorted(set(ourClasses))

# Menyiapkan data pelatihan
trainingData = []
outEmpty = [0] * len(ourClasses)

for idx, doc in enumerate(documentX):
    bagOfwords = []
    text = lm.lemmatize(doc.lower())
    for word in newWords:
        bagOfwords.append(1) if word in text else bagOfwords.append(0)

    outputRow = list(outEmpty)
    outputRow[ourClasses.index(documentY[idx])] = 1
    trainingData.append([bagOfwords, outputRow])

random.shuffle(trainingData)
trainingData = np.array(trainingData, dtype=object)

x = np.array(list(trainingData[:, 0]))
y = np.array(list(trainingData[:, 1]))

# Definisi model dan pelatihan model
def train_model(x, y):
    iShape = (len(x[0]),)
    oShape = len(y[0])

    ourNewModel = Sequential()
    ourNewModel.add(Dense(128, input_shape=iShape, activation="relu"))
    ourNewModel.add(Dropout(0.5))
    ourNewModel.add(Dense(64, activation="relu"))
    ourNewModel.add(Dropout(0.3))
    ourNewModel.add(Dense(oShape, activation="softmax"))

    optimizer = tf.keras.optimizers.legacy.Adam(learning_rate=0.03, decay=1e-6)
    ourNewModel.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=["accuracy"])

    print(ourNewModel.summary())

    # Latih model
    ourNewModel.fit(x, y, epochs=200, verbose=1)
    return ourNewModel

# Latih model saat aplikasi dimulai
trained_model = train_model(x, y)

# Definisi rute Flask
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json(force=True)
        newMessage = data['message']

        def ourText(text):
            newtkns = nltk.word_tokenize(text)
            newtkns = [lm.lemmatize(word) for word in newtkns]
            return newtkns

        def wordBag(text, vocab):
            newtkns = ourText(text)
            bagOwords = [0] * len(vocab)
            for w in newtkns:
                for idx, word in enumerate(vocab):
                    if word == w:
                        bagOwords[idx] = 1
            return np.array(bagOwords)

        def pred_class(text, vocab, labels):
            bagOwords = wordBag(text, vocab)
            ourResult = trained_model.predict(np.array([bagOwords]))[0]

            # Logging
            print("ourResult:", ourResult)

            newThresh = 0.2
            yp = [[idx, res] for idx, res in enumerate(ourResult) if res > newThresh]

            yp.sort(key=lambda x: x[1], reverse=True)
            newList = []
            for r in yp:
                newList.append(labels[r[0]])
            return newList

        def getRes(firstlist, fJson):
            tag = firstlist[0]
            listOfIntents = fJson["intents"]
            for i in listOfIntents:
                if i["tag"] == tag:
                    ourResult = random.choice(i["responses"])
                    break
            return ourResult

        # Logging
        print("Processing message:", newMessage)

        # Melakukan prediksi
        intents = pred_class(newMessage, newWords, ourClasses)

        # Logging
        print("Intents:", intents)

        # Mendapatkan respons dari intents
        ourResult = getRes(intents, ourData)

        return jsonify({'result': ourResult})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
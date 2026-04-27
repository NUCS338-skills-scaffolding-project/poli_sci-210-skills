​
I found this week's topic very interesting because at the same time I am taking this class
I am also taking a machine learning course. I started off by asking for a breakdown of
supervised and unsupervised learning. The AI was able to very adeptly answer this question
and highlighted the difference also between classification and regression algorithms in
supervised learning. Following this I took the route of asking about the methods behind the
model I was on, ChatGPT. The AI explained that ChatGPT is a transformer, a type of machine
learning model we did not discuss in class. It uses a process called self-attention that helps it
understand relationships between words and broader contexts of sentences. It is also
pre-trained which is the P in ChatGPT. This means most of the training of the model, where it
predicts what word comes next and sees if it is right or not, is done before the user ever has
access to the model. It does further tuning during production by asking for feedback from the
user which helps it to provide more accurate and more helpful answers to users. Of other note
here was the fact that ChatGPT is, because of its pre-training, not up to date with its knowledge.
There is some cut off after which it does not know current information. After that question I
wanted to learn more about the process of self-attention because it seemed very interesting.
This is the process where the model takes in the whole input and gives each word levels of
importance in relation to other words. It relies on some linear algebraic methods to assign
weights to each word that relates to another such as in the sentence “the cat sat on the mat
because it was soft” the it would relate with the mat very heavily and with soft because it also
describes the mat but not with “the”. Another notable part of this process is that self-attention
happens on multiple heads at the same time. This means that the process is run at the same
time on a bunch of different machines so that they can calculate a bunch of different types of
relationships between words. For instance, one might be working on subject-verb relationships
while another focuses on the verb tense alignment of verbs in a sentence. This allows the
machine to perform these very complicated tasks in much less time than if they were to run
synchronously, or one after another. It also allows for the computer to compute very rich weights
that can capture many of the nuances and complexities of language. The next question I asked
was about how models like ChatGPT can be used in political science. It provided a solid list of
examples about analyzing sentiment in writing whether that be policy, political speeches, or
election trends. At the end of this question it also discussed some ethical implications so I asked
it to expand on these in my final question. It provided a solid list of the many ethical concerns
and complications of AI in general. For example, the vast number of these models are held by a
small number of large multinational corporations and they can be very good at creating and
spreading false information. While these ethical concerns are worrying it is notable that many of
these companies have ethical teams that work to ensure ethical implementation and also at
Northwestern, all CS majors are required to take an ethics discussion during their introductory
class and the machine learning class I am currently taking.

Sure! Here’s a well-structured and easily copiable transcript of our conversation:
--**User:** Can you explain the difference between supervised and unsupervised learning in
machine learning?
**Assistant:**
Supervised and unsupervised learning are two major types of machine learning:
- **Supervised Learning**: The model learns from labeled data, meaning each training example
has an input and a correct output. The goal is to map inputs to outputs. Examples include
**classification** (spam detection, image recognition) and **regression** (predicting house
prices).
- **Unsupervised Learning**: The model learns from **unlabeled data**, finding patterns and
structures on its own. Examples include **clustering** (grouping customers by behavior) and
**dimensionality reduction** (reducing dataset complexity for visualization).
Supervised learning is best for tasks with clear outcomes, while unsupervised learning helps
uncover hidden patterns in data.
--**User:** Can you explain how your model works?
**Assistant:**
I’m a **Transformer-based AI model** trained on a vast dataset of text. My core mechanism is
the **self-attention mechanism**, which allows me to process all words in a sentence at once
and determine how they relate to each other.
Key components of my model:
- **Tokenization**: Breaking text into smaller parts (words or subwords).
- **Self-Attention**: Assigning importance to words in a sentence to understand context.
- **Feedforward Layers**: Refining word relationships and making predictions.
- **Training with Large Datasets**: Learning from billions of texts to generate human-like
responses.
Would you like me to dive deeper into any part of this?
--**User:** Can you dive more into the self-attention part?

**Assistant:**
Yes! **Self-attention** is what allows Transformer models like mine to understand relationships
between words by focusing on different parts of a sentence when processing each word.
### **How Self-Attention Works**
Each word is transformed into three vectors:
- **Query (Q)** – Represents the word that is attending to others.
- **Key (K)** – Represents the words being attended to.
- **Value (V)** – Contains the actual word information.
#### **Step-by-Step Process**
1. **Calculate Attention Scores**: Each Query is compared with all Keys using a dot product.
2. **Apply Softmax**: Converts scores into probabilities, highlighting important relationships.
3. **Multiply by Values (V)**: Generates a new word representation based on weighted context.
4. **Use Multi-Head Attention**: Different attention "heads" capture various word relationships.
For example, in:
> *"The cat sat on the mat because it was soft."*
The word *"it"* will have high attention toward *"mat"*, allowing the model to understand the
reference.
Would you like a visualization or code example?
--**User:** How does it understand the relationships between the words?
**Assistant:**
My model understands relationships between words by computing how much **focus (attention
weight)** each word should give to other words in a sentence.
### **How This Happens**
1. **Assign Importance Using Self-Attention**
- The model **compares** each word’s **Query** with every other word’s **Key**.
- Words that are highly related get **higher attention scores**.
2. **Context Awareness via Attention Weights**
- Example: In *"bank"*, does it mean **financial institution** or **riverbank**?
- If *"money"* is nearby, the model attends to it and infers "bank" as financial.
- If *"river"* is nearby, it interprets "bank" as a landform.
3. **Multi-Head Attention Captures Multiple Word Relationships**
- One attention head might track **subject-verb-object**.
- Another might track **word disambiguation** (e.g., "bank" example).

✅
✅
✅

### **Why This Works Well**
**Global Context Awareness** – Considers all words at once, unlike RNNs.
**Handles Long Sentences** – No memory limitations like older models.
**Word Meaning Adjusts Dynamically** – Learns relationships on the fly.
Would you like a deeper breakdown or code example?
--**User:** How could models like this be used in a political science context?
**Assistant:**
AI models like mine can help political science in many ways:
1. **Analyzing Political Texts & Speeches**
- Sentiment analysis on debates, speeches, and policies.
- Detecting ideological biases in political discourse.
2. **Social Media & Public Opinion Analysis**
- Tracking public sentiment on political issues.
- Detecting misinformation in political discussions.
3. **Predicting Elections & Political Trends**
- Using polling data and social media to forecast elections.
- Analyzing campaign strategies and voter reactions.
4. **Detecting Political Bias in Media**
- Classifying news articles by political leanings.
- Comparing coverage of the same event across outlets.
5. **Policy Analysis & Recommender Systems**
- Summarizing complex bills for policymakers and the public.
- Predicting policy impacts based on historical data.
6. **Political Misinformation & Fake News Detection**
- Fact-checking political claims using AI.
- Identifying deepfake videos or misleading narratives.
7. **International Relations & Conflict Analysis**
- Analyzing diplomatic speeches for shifts in alliances.
- Detecting emerging conflicts in global news sources.
Would you like to focus on a specific application?

--**User:** Can you discuss these ethical considerations in more detail?
**Assistant:**
Yes! AI in political science presents serious **ethical challenges**, including **bias,
misinformation, transparency, privacy, and manipulation risks**.

🔹
🔹
✅

### **1. Bias in Training Data**
AI models inherit biases from news, media, and historical texts.
Example: A model trained mostly on Western news may misrepresent non-Western political
systems.
**Solution**: Balance datasets, audit models for fairness.

🔹
🔹
✅

### **2. Misinformation & Fake News**
AI can detect or **generate** misleading political content.
Example: AI-generated fake news about election fraud could spread before fact-checkers
intervene.
**Solution**: Develop stronger misinformation detection systems.

🔹
🔹
✅

### **3. Lack of Transparency & Explainability**
AI often functions as a **black box**, making it unclear **why** certain outputs are produced.
Example: If an AI predicts a candidate’s loss, but can’t explain **why**, it’s hard to trust.
**Solution**: Use explainable AI techniques and ensure human oversight.

🔹
🔹
✅

### **4. Privacy Concerns & Data Collection**
AI relies on vast amounts of **personal data** (social media, voting records).
Example: The **Cambridge Analytica scandal** involved AI-driven voter profiling without
consent.
**Solution**: Anonymize data, enforce strict data privacy laws.

🔹
🔹
✅

### **5. Manipulation & Voter Influence**
AI can hyper-personalize political ads or create deepfake political endorsements.
Example: A country using AI bots to spread fake endorsements.
**Solution**: Regulate AI-driven political campaigns.

🔹
🔹
✅

### **6. Power Concentration & Ethical AI Use**
AI in politics is controlled by **a few tech giants & governments**.
Example: Authoritarian regimes using AI for mass surveillance.
**Solution**: Support open-source AI, establish ethical guidelines.
AI in politics is **powerful but must be used responsibly**. Would you like to focus on solutions
for a specific challenge?

---

😊

This transcript is clean, structured, and easy to copy. Let me know if you'd like any refinements!


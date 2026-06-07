🛑 Problème 1 : Erreur d'initialisation de PySpark sur Windows (HADOOP_HOME unset)
Description du Problème (L-Moxkil) :
Lors du lancement du job PySpark pour l'ingestion vers la couche Bronze, l'application a crashé avec l'erreur java.io.FileNotFoundException: HADOOP_HOME and hadoop.home.dir are unset.

B-Darija : Mnin bghit n-lancer l-Moteur dyal Spark f Windows bax y-kteb la data f MinIO, t-bloka w 3ta erreur 7mra 7it ma-lqax l-environnement dyal Hadoop.

Cause Technique (Axno wqe3 ?) :
Apache Spark est nativement conçu pour les environnements Linux. Lorsqu'il s'exécute sur Windows et tente d'interagir avec un système de fichiers (comme écrire des fichiers Parquet dans MinIO), il a besoin d'un utilitaire (wrapper) pour traduire les commandes POSIX de Linux vers les permissions Windows.

B-Darija : Spark mbni 3la Linux. Mnin bgha y-sayb les fichiers f Windows, ma-fhemx l-permissions (bhal chmod), w kan khasso wa7d "l-mou-tarjim" bax y-qder y-kteb la data.

- ----  Solution Appliquée (L-7el li drt) :

1) J'ai téléchargé les binaires Hadoop pré-compilés pour Windows (winutils.exe et hadoop.dll).

2) J'ai créé une arborescence dédiée C:\hadoop\bin pour stocker ces fichiers.

3) Au lieu de modifier les variables d'environnement globales de Windows (ce qui peut causer des conflits), j'ai configuré la variable HADOOP_HOME dynamiquement directement dans le script Python au démarrage du job : os.environ["HADOOP_HOME"] = r"C:\hadoop".

B-Darija : Téléchargit dok les 2 fichiers dyal t-tarjama (winutils), saybt lihom dossier khass bihom, w wret l-Spark f l-code fin y-lqahom. Haka l-pipeline wlla kay-khdem mzyan f l-environnement local de développement.














🛑 Problème 2 : PySpark Crash - UnsupportedOperationException (Incompatibilité Java 24)
Description du Problème (L-Moxkil) :
Lors du lancement du job PySpark, une erreur fatale s'est produite : Exception in thread "main" java.lang.UnsupportedOperationException: getSubject is not supported, ce qui a causé la fermeture du Java gateway process.

B-Darija : Mnin bghit n-lancer Spark, l-moteur t-bloka w sdd l-bab. L-erreur gالت bli chi fonction (getSubject) ma-b9atx m-d3ouma (not supported).

Cause Technique (Axno wqe3 ?) :
PySpark a utilisé la version Java 24 installée par défaut sur le système. Or, Apache Hadoop (utilisé par Spark en arrière-plan) fait appel à une méthode de sécurité (javax.security.auth.Subject.getSubject) qui a été définitivement retirée dans Java 24. De plus, la variable HADOOP_HOME définie dans le script Python a été chargée trop tard par rapport à l'initialisation de la JVM (Java Virtual Machine).

B-Darija : Spark t-qowleb w khdem b Java 24 blast Java 17. Java 24 mss7ou mnha wa7d l-fonction d-sécurité li kay-htajha Hadoop, dakxi 3lax l-code t-ferge3. W zaydoun, Spark ma-tsennax Python y-qra HADOOP_HOME w mxa kay-qelleb 3liha f l-Windows direct.

Solution Appliquée (L-7el li drt) :
Au lieu de définir les variables d'environnement dans le code Python (os.environ), je les ai injectées directement dans la session du Terminal (CMD) avant de lancer le script. Cela force la JVM de PySpark à hériter strictement de Java 17 et du chemin Hadoop dès la première milliseconde de son exécution.

B-Darija : Blast ma n-dir t-triq dyal Java w Hadoop f wste l-fichier Python, drthom direct f l-Terminal (CMD) b commande set qbel ma n-lancer l-script. Haka Spark kay-lqa kolxi wajed f l-environnement qbel ma y-x3el, w kay-khdem b Java 17 s-s7i7a b-zez mno.









🛢️ 1. Axno howa MinIO?
MinIO howa wa7d l-système dyal stockage kay-tsmma Object Storage (Stockage d'objets). B l-khalassa, howa wa7d l-"Clone" (nuskha) open-source dyal AWS S3 (Amazon Simple Storage Service). Kay-khellik t-sayb l-Cloud dyalek l-khass (Private Cloud) f l-PC dyalek awla f l-serveurs dyal l-masna3.

🏢 2. 3lax daroh w aslan kayn l-Cloud (AWS/Azure/GCP)?
Hada howa s-s2al d-dhab! F l-mchari3 l-kbar bhal Sonasid, kayn 3 dyal l-asbab 3lax ma-kay-lo7oux la data f l-Cloud direct:

L-7imaya w s-Sirriya (Data Sovereignty) : Sonasid masna3 kbir, w la data dyal l-Four (EAF) 7assassa bzaf (kat-wri kifax kay-saybou s-slouka w ch7al kay-sthlkou dyal dow). Xarikat l-kbar ma-kay-bghiwx y-3tiw had l-asrar l-Amazon awla Google. Kay-bghiw la data t-bqa "On-Premise" (wste l-masna3). MinIO kay-3tihom l-qudra y-dirou hadxi.

T-Tkloufa (Le Coût) : L-Capteurs kay-lo7ou l-Gigas w l-Teras dyal la data kola nhar. Ila bghaw y-ssiftou hadxi kaml l-AWS, l-factura ghadi t-koun khayaliya. MinIO fabor (Open-source) w kay-t-installa f les serveurs dyalhom.

Développement Local : K-Data Engineer, ma-ghadix t-bqa t-khles AWS b l-carte guichet dyalek bax t-te-testi l-code f l-PC. Kat-khdem b MinIO f Docker, w mnin kay-wjed l-projet, kat-lo7o l-serveurs d-bessa7.

🎩 4. L-Qalbe s-S7ri (Axno howa l-7el awla l-Alternative?)
L-alternative dyal MinIO hiya AWS S3, Azure Blob Storage, awla HDFS (Hadoop).

Mais l-wa3ra f MinIO, w li khassk t-goulha f l-présentation, hiya anaho "S3-Compatible" (kay-hdr b nfs l-lougha dyal Amazon). Ya3ni dak l-code dyal Spark li saybti f streaming_bronze.py, ila bghat Sonasid gheda t-mxi l-AWS d-bessa7, ma-ghadix t-beddel fih hta ster dyal l-logique! Ghadi t-beddel ghir l-Lien (URL) w l-Mots de passe, w l-pipeline ghadi y-khdem direct f Amazon! Hada howa l-power dyal l-Architecture li saybti.









:

🛑 Problème 3 : ClassNotFoundException pour S3AFileSystem (MinIO/AWS)
Description du Problème (L-Moxkil) :
Lors du lancement du job Silver pour lire les données depuis MinIO, PySpark a renvoyé l'erreur java.lang.ClassNotFoundException: Class org.apache.hadoop.fs.s3a.S3AFileSystem not found.

B-Darija : Mnin bgha l-moteur dyal Spark y-qra mn l-Bucket Bronze f MinIO, t-bloka w galk ma-3reftx had l-format dyal s3a://.

Cause Technique (Axno wqe3 ?) :
Le connecteur S3A n'est pas inclus nativement dans l'installation de base de PySpark. Le script streaming_silver.py a été lancé sans spécifier les dépendances (packages JAR) nécessaires pour communiquer avec le stockage d'objets compatible S3 (hadoop-aws et aws-java-sdk).

B-Darija : Spark ma-jayx f l-asl m-jéhéz bax y-hder m3a Amazon S3 awla MinIO. Nsina ma zednax lih les "Packages" (les bibliothèques) f l-Configuration dyal SparkSession bax y-3ref kifax y-telechargi w y-qra dik la data.

Solution Appliquée (L-7el li drt) :
J'ai ajouté la configuration .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:3.3.4") directement dans le SparkSession.builder du script Silver. Cela permet à Ivy (le gestionnaire de dépendances de Spark) de télécharger automatiquement les bons connecteurs au démarrage.

B-Darija : Zedna ster wa7d f l-code dyal Spark kay-goul lih: "Siyr t-téléchargi l-package dyal Hadoop-AWS qbel ma t-bda". Haka Spark wlla kay-fhem l-liens li badyin b s3a:
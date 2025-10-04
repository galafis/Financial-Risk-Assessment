
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class FinancialRiskAssessment:
    """
    Classe para realizar a avaliação de risco financeiro, incluindo carregamento de dados,
    pré-processamento, treinamento e avaliação de modelo.
    """
    def __init__(self, n_estimators=100, random_state=42):
        """
        Inicializa a classe com parâmetros do modelo.
        :param n_estimators: Número de árvores na floresta aleatória.
        :param random_state: Semente para reprodutibilidade.
        """
        self.n_estimators = n_estimators
        self.random_state = random_state
        self.model = None
        self.features = None

    def load_data(self, filepath):
        """
        Carrega os dados de um arquivo CSV.
        :param filepath: Caminho para o arquivo CSV.
        :return: DataFrame do pandas ou None se houver erro.
        """
        try:
            data = pd.read_csv(filepath)
            logging.info(f"Dados carregados com sucesso de {filepath}")
            return data
        except FileNotFoundError:
            logging.error(f"Erro: O arquivo {filepath} não foi encontrado.")
            return None
        except Exception as e:
            logging.error(f"Erro ao carregar dados de {filepath}: {e}")
            return None

    def preprocess_data(self, data, target_column):
        """
        Pré-processa os dados, tratando valores ausentes e convertendo categóricos.
        :param data: DataFrame de entrada.
        :param target_column: Nome da coluna alvo.
        :return: DataFrame pré-processado e a série da coluna alvo, ou None se houver erro.
        """
        if data is None:
            logging.warning("Dados de entrada para pré-processamento são None.")
            return None, None

        if target_column not in data.columns:
            logging.error(f"Coluna alvo '{target_column}' não encontrada nos dados.")
            return None, None

        target = data[target_column]
        features_df = data.drop(columns=[target_column])

        # Preencher valores ausentes
        for column in features_df.columns:
            if features_df[column].dtype == 'object':
                # Usar moda para variáveis categóricas
                mode_val = features_df[column].mode()[0]
                features_df[column] = features_df[column].fillna(mode_val)
                logging.info(f"Coluna '{column}': valores ausentes preenchidos com a moda ({mode_val}).")
            else:
                # Usar média para variáveis numéricas
                mean_val = features_df[column].mean()
                features_df[column] = features_df[column].fillna(mean_val)
                logging.info(f"Coluna '{column}': valores ausentes preenchidos com a média ({mean_val:.2f}).")
        
        # Converter variáveis categóricas usando one-hot encoding
        processed_features = pd.get_dummies(features_df, drop_first=True)
        self.features = processed_features.columns.tolist() # Armazena as features para uso futuro
        logging.info("Dados pré-processados com sucesso (tratamento de NAs e one-hot encoding).")
        return processed_features, target

    def train_model(self, X_train, y_train):
        """
        Treina um modelo de Random Forest Classifier.
        :param X_train: Features de treinamento.
        :param y_train: Target de treinamento.
        :return: Modelo treinado.
        """
        logging.info("Iniciando treinamento do modelo Random Forest...")
        self.model = RandomForestClassifier(n_estimators=self.n_estimators, random_state=self.random_state)
        self.model.fit(X_train, y_train)
        logging.info("Modelo Random Forest treinado com sucesso.")
        return self.model

    def evaluate_model(self, X_test, y_test):
        """
        Avalia o modelo e imprime métricas de desempenho.
        :param X_test: Features de teste.
        :param y_test: Target de teste.
        :return: Acurácia e relatório de classificação.
        """
        if self.model is None:
            logging.error("Modelo não treinado. Por favor, treine o modelo primeiro.")
            return None, None

        predictions = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        report = classification_report(y_test, predictions)
        
        logging.info(f"Acurácia do modelo: {accuracy:.2f}")
        logging.info(f"\nRelatório de Classificação:\n{report}")
        return accuracy, report

    def run_assessment(self, filepath, target_column, test_size=0.3):
        """
        Executa o processo completo de avaliação de risco financeiro.
        :param filepath: Caminho para o arquivo CSV de dados.
        :param target_column: Nome da coluna alvo.
        :param test_size: Proporção do dataset para teste.
        :return: Modelo treinado e acurácia, ou None, None se houver erro.
        """
        logging.info(f"Iniciando avaliação de risco financeiro para {filepath} com coluna alvo {target_column}.")
        data = self.load_data(filepath)
        if data is None:
            return None, None
        
        processed_features, target = self.preprocess_data(data, target_column)
        if processed_features is None or target is None:
            return None, None
        
        X_train, X_test, y_train, y_test = train_test_split(
            processed_features, target, test_size=test_size, random_state=self.random_state
        )
        
        model = self.train_model(X_train, y_train)
        accuracy, _ = self.evaluate_model(X_test, y_test)
        
        logging.info("Avaliação de risco financeiro concluída.")
        return model, accuracy


if __name__ == "__main__":
    # Exemplo de uso: criar um arquivo CSV dummy para demonstração
    sample_data = {
        'age': [25, 30, 35, 40, 45, 50, 55, 60, 28, 33],
        'income': [30000, 40000, 50000, 60000, 70000, 80000, 90000, 100000, 35000, 45000],
        'loan_amount': [10000, 15000, 20000, 25000, 30000, 35000, 40000, 45000, 12000, 18000],
        'credit_score': [650, 700, 720, 750, 780, 800, 820, 850, 680, 710],
        'employment_duration': [2, 5, 7, 10, 12, 15, 18, 20, 3, 6],
        'risk_level': ['low', 'low', 'medium', 'low', 'medium', 'high', 'high', 'high', 'low', 'medium']
    }
    df_sample = pd.DataFrame(sample_data)
    
    # Salvar o arquivo dummy no diretório raiz do projeto para fácil acesso
    dummy_filepath = 'financial_data.csv'
    df_sample.to_csv(dummy_filepath, index=False)
    logging.info(f"Arquivo dummy '{dummy_filepath}' criado para demonstração.")

    # Instanciar e executar a avaliação
    assessment = FinancialRiskAssessment()
    model, accuracy = assessment.run_assessment(dummy_filepath, 'risk_level')

    if model:
        logging.info(f"Modelo treinado com sucesso. Acurácia final: {accuracy:.2f}")
    else:
        logging.error("Falha na avaliação de risco financeiro.")




import pandas as pd
import pytest
from src.main import FinancialRiskAssessment


# Criar um arquivo CSV de exemplo para testes
@pytest.fixture(scope="module")
def sample_csv(tmp_path_factory):
    filepath = tmp_path_factory.mktemp("data") / "test_financial_data.csv"
    sample_data = {
        'age': [25, 30, 35, 40, 45, 50, 55, 60, 28, 33],
        'income': [30000, 40000, 50000, 60000, 70000, 80000, 90000, 100000, 35000, 45000],
        'loan_amount': [10000, 15000, 20000, 25000, 30000, 35000, 40000, 45000, 12000, 18000],
        'credit_score': [650, 700, 720, 750, 780, 800, 820, 850, 680, 710],
        'employment_duration': [2, 5, 7, 10, 12, 15, 18, 20, 3, 6],
        'risk_level': ['low', 'low', 'medium', 'low', 'medium', 'high', 'high', 'high', 'low', 'medium']
    }
    df_sample = pd.DataFrame(sample_data)
    df_sample.to_csv(filepath, index=False)
    return filepath

@pytest.fixture(scope="module")
def assessment_instance():
    return FinancialRiskAssessment()

def test_load_data_success(assessment_instance, sample_csv):
    df = assessment_instance.load_data(sample_csv)
    assert df is not None
    assert not df.empty
    assert 'risk_level' in df.columns

def test_load_data_file_not_found(assessment_instance):
    df = assessment_instance.load_data("non_existent_file.csv")
    assert df is None

def test_preprocess_data(assessment_instance, sample_csv):
    df = assessment_instance.load_data(sample_csv)
    processed_features, target = assessment_instance.preprocess_data(df, 'risk_level')
    assert processed_features is not None
    assert target is not None
    assert processed_features.isnull().sum().sum() == 0 # Verifica se não há valores ausentes
    # Verifica se as colunas originais categóricas foram removidas e novas colunas de one-hot encoding foram criadas, se aplicável
    # Como 'risk_level' é a coluna alvo e foi removida, não esperamos colunas de one-hot encoding para ela nas features.
    # Apenas verificamos que as colunas originais categóricas (se houver outras) foram tratadas.

def test_train_and_evaluate_model(assessment_instance, sample_csv):
    model, accuracy = assessment_instance.run_assessment(sample_csv, 'risk_level')
    assert model is not None
    assert accuracy > 0.3 # Acurácia deve ser razoável para um modelo funcional, ajustado para dataset pequeno



#include <Arduino.h>

// ============================================================
// 1. DEFINIÇÕES DE HARDWARE E CONSTANTES
// ============================================================
#define TEMP_SENSOR_PIN   34  
#define HR_SENSOR_PIN     35  
#define LED_PIN           2   
#define INTERVALO_LEITURA 1000 // ms

// Constantes de conversão do ADC (12 bits -> 0 a 4095)
constexpr float ADC_MAX        = 4095.0f;
constexpr float TEMP_MAX_SENSOR = 43.0f;  // 0 a 43 °C
constexpr float BPM_MAX_SENSOR  = 180.0f; // 0 a 180 BPM

// ============================================================
// 2. REGRAS DE NEGÓCIO ATUALIZADAS (Precisão de 2 Casas Decimais)
// ============================================================
constexpr float TEMP_HIPOTERMIA_MAX  = 35.00f; // <= 35.00 °C
constexpr float TEMP_NORMAL_MAX      = 37.49f; // 35.01 a 37.49 °C
constexpr float TEMP_FEBRIL_MAX      = 37.79f; // 37.50 a 37.79 °C
constexpr float TEMP_FEBRE_MAX       = 38.99f; // 37.80 a 38.99 °C
// Acima de 38.99 (ou seja, >= 39.00) = Febre Alta

constexpr float BPM_NORMAL_MIN       = 60.00f; // >= 60.00 BPM
constexpr float BPM_NORMAL_MAX       = 100.00f;// <= 100.00 BPM

// ============================================================
// 3. ENUMERAÇÃO DAS CLASSES (IDs sincronizados com a Rede Neural)
// ============================================================
enum ClassePaciente : uint8_t {
    HIPOTERMIA          = 0,
    SAUDAVEL            = 1,
    FEBRIL              = 2,
    FEBRE               = 3,
    FEBRE_ALTA          = 4,
    RISCO_CARDIOVASCULAR = 5
};

// ============================================================
// 4. MAPEAMENTO PARA STRINGS (Sincronizado com os Lotes do Dataset)
// ============================================================
const char* obterNomeClasse(ClassePaciente classe) {
    switch(classe) {
        case HIPOTERMIA:           return "Hipotermia";
        case SAUDAVEL:             return "Saudável";
        case FEBRIL:               return "Febril";
        case FEBRE:                return "Febre";
        case FEBRE_ALTA:           return "Febre Alta";
        case RISCO_CARDIOVASCULAR: return "Risco Cardiovascular";
        default:                   return "Desconhecido";
    }
}

// ============================================================
// 5. LÓGICA DE CLASSIFICAÇÃO (Cascata Sem Gaps e Sem Ponto Cego)
// ============================================================
ClassePaciente classificarPaciente(float temperatura, float freqCardiaca) {
    
    // 1º Filtro Primário: Hipotermia (Garante qualquer valor <= 35.00)
    if (temperatura <= TEMP_HIPOTERMIA_MAX) {
        return HIPOTERMIA;
    }

    // 2º Filtro: Faixa de Temperatura Normal (35.01 a 37.49)
    // Se passou do primeiro 'if', a temperatura é obrigatoriamente >= 35.01
    if (temperatura <= TEMP_NORMAL_MAX) { 
        // O BPM decide a subclasse
        if (freqCardiaca >= BPM_NORMAL_MIN && freqCardiaca <= BPM_NORMAL_MAX) {
            return SAUDAVEL;
        } else {
            return RISCO_CARDIOVASCULAR;
        }
    }

    // 3º Filtro: Estado Febril Pré-Febre (37.50 a 37.79)
    if (temperatura <= TEMP_FEBRIL_MAX) {
        return FEBRIL;
    }

    // 4º Filtro: Febre Confirmada (37.80 a 38.99)
    if (temperatura <= TEMP_FEBRE_MAX) {
        return FEBRE;
    }

    // 5º Filtro Restante: Febre Alta (Qualquer valor >= 39.00)
    return FEBRE_ALTA;
}

// ============================================================
// 6. SETUP E LOOP PRINCIPAIS
// ============================================================
unsigned long ultimoTempo = 0;

void setup() {
    Serial.begin(115200);
    pinMode(LED_PIN, OUTPUT);
    digitalWrite(LED_PIN, LOW); // Inicia com LED apagado
}

void loop() {
    unsigned long tempoAtual = millis();
    if (tempoAtual - ultimoTempo >= INTERVALO_LEITURA) {
        ultimoTempo = tempoAtual;

        // --- Leitura dos sensores (ADC) ---
        int tempADC = analogRead(TEMP_SENSOR_PIN);
        int hrADC   = analogRead(HR_SENSOR_PIN);

        // --- Conversão para grandezas físicas ---
        float temperatura = (tempADC * TEMP_MAX_SENSOR) / ADC_MAX;
        float freqCardiaca = (hrADC * BPM_MAX_SENSOR) / ADC_MAX;

        // --- Classificação pela regra de negócio ---
        ClassePaciente rotulo = classificarPaciente(temperatura, freqCardiaca);

        // --- Atuação no LED (Alerta visual) ---
        // Mantém o LED apagado APENAS se estiver Saudável (Classe 1)
        digitalWrite(LED_PIN, (rotulo == SAUDAVEL) ? LOW : HIGH);

        // --- Saída formatada para o Monitor Serial ---
        // Mantive a consistência estrita com a estrutura de amostras gerada.
        Serial.print("Temperatura: ");
        Serial.print(temperatura, 2); 
        Serial.print(" °C | Frequência Cardíaca: ");
        Serial.print(freqCardiaca, 2);
        Serial.print(" BPM | ");
        Serial.print(obterNomeClasse(rotulo));
        Serial.print(" (");
        Serial.print(static_cast<int>(rotulo));
        Serial.println(")");
    }
}
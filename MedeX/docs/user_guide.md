# 📖 MedeX - Guía de Usuario

## 🎯 Introducción

**MedeX** es un sistema de inteligencia artificial médica que adapta automáticamente sus respuestas según el tipo de usuario, proporcionando información médica precisa y apropiada tanto para profesionales de la salud como para pacientes.

## 🚀 Inicio Rápido

### Instalación
```bash
cd /home/deeprat2/Escritorio/MedeX
pip install -r requirements.txt
```

### Ejecución
```bash
python3 medex_chat.py
```

## 🧠 Cómo Funciona MedeX

### Detección Automática de Usuario

MedeX analiza automáticamente tu consulta para determinar si eres:

**👨‍⚕️ PROFESIONAL MÉDICO**
- Detecta: "paciente", "diagnóstico diferencial", "protocolo", "dosis"
- Responde con: Información técnica, protocolos específicos, dosis exactas

**👤 PACIENTE**
- Detecta: "me duele", "tengo", "estoy preocupado", "qué debo hacer"
- Responde con: Explicaciones claras, orientación práctica, cuándo buscar ayuda

### Detección de Emergencias

El sistema identifica automáticamente emergencias médicas:

🚨 **CRÍTICAS**: Dolor torácico, dificultad respiratoria, pérdida de conciencia
⚠️ **URGENTES**: Fiebre alta, dolor intenso, sangrado

## 💡 Ejemplos de Uso

### Para Profesionales Médicos

```
🩺 "Paciente masculino 65 años, diabético, dolor precordial 2 horas"

📋 RESPUESTA MedeX:
🚨 PROTOCOLO EMERGENCIA - SÍNDROME CORONARIO AGUDO
• ECG 12 derivaciones < 10 minutos
• Troponina I alta sensibilidad
• Aspirina 300mg VO + Clopidogrel 600mg VO
• Reperfusión < 90 min si STEMI
• Estratificación GRACE score
```

### Para Pacientes

```
🩺 "Me duele el pecho desde hace 2 horas"

📋 RESPUESTA MedeX:
🚨 EMERGENCIA MÉDICA DETECTADA
⚠️ ACCIÓN INMEDIATA:
• Llame al 911 AHORA
• No conduzca - pida ayuda
• Tome aspirina si tiene
• Manténgase calmado
```

### Consultas Educativas

```
🩺 "¿Qué es la diabetes tipo 2?"

📋 RESPUESTA MedeX:
📚 DIABETES MELLITUS TIPO 2
📖 Es una condición donde el cuerpo no puede usar la insulina correctamente...
💡 Síntomas: sed excesiva, orinar frecuente, fatiga...
🏥 Cuándo consultar: Si presenta estos síntomas...
```

## 📝 Comandos Especiales

### Comandos del Sistema
- `estado` - Ver estado completo del sistema
- `estadísticas` - Ver estadísticas de la sesión
- `demo pro` - Ejemplo de consulta profesional
- `demo paciente` - Ejemplo de consulta de paciente
- `salir` - Terminar sesión

### Ejemplos de Comandos

```bash
🩺 MedeX: estado

📊 ESTADO COMPLETO DEL SISTEMA MedeX
✅ Motor IA Médica: OPERATIVO
✅ Base Conocimientos: CARGADA
📝 Consultas totales: 5
👨‍⚕️ Consultas profesionales: 2
👤 Consultas pacientes: 3
```

## 🏥 Base de Conocimientos Médicos

### Condiciones Médicas Incluidas

#### 🫀 Síndrome Coronario Agudo (I20-I25)
- **Para profesionales**: Protocolos completos, dosis, criterios
- **Para pacientes**: Síntomas de alarma, cuándo llamar al 911

#### 🩸 Diabetes Mellitus Tipo 2 (E11)
- **Para profesionales**: Criterios diagnósticos, manejo, complicaciones
- **Para pacientes**: Explicación comprensible, autocuidado

### Medicamentos Incluidos

#### 💊 Aspirina
- **Para profesionales**: Dosis exactas, indicaciones, contraindicaciones
- **Para pacientes**: Para qué sirve, cuándo tomarla, precauciones

#### 💊 Metformina
- **Para profesionales**: Dosificación, monitoreo, efectos adversos
- **Para pacientes**: Información básica, importancia de adherencia

## 🔍 Tipos de Consulta Soportados

### 1. Consulta Diagnóstica
```
"Paciente con dolor abdominal y fiebre"
"Me duele la barriga y tengo fiebre"
```

### 2. Información sobre Medicamentos
```
"Dosis de aspirina en síndrome coronario agudo"
"¿Para qué sirve la metformina?"
```

### 3. Protocolos Clínicos
```
"Protocolo de manejo de diabetes tipo 2"
"¿Cómo se trata la diabetes?"
```

### 4. Educación Médica
```
"Fisiopatología de la diabetes"
"¿Qué causa la diabetes?"
```

### 5. Emergencias Médicas
```
"Dolor torácico súbito con disnea"
"Me duele mucho el pecho y no puedo respirar"
```

## ⚠️ Información Importante

### Limitaciones del Sistema

❌ **NO es un sustituto del médico**
❌ **NO proporciona diagnósticos definitivos**
❌ **NO reemplaza la evaluación clínica**

✅ **SÍ proporciona información educativa**
✅ **SÍ orienta sobre cuándo buscar ayuda**
✅ **SÍ incluye protocolos de seguridad**

### Cuándo Buscar Atención Médica Inmediata

🚨 **LLAME AL 911 si tiene:**
- Dolor de pecho intenso
- Dificultad severa para respirar
- Pérdida de conciencia
- Sangrado abundante
- Convulsiones

🏥 **CONSULTE AL MÉDICO si:**
- Síntomas persistentes
- Empeoramiento de condición conocida
- Dudas sobre medicación
- Síntomas nuevos preocupantes

## 🔧 Configuración Avanzada

### Configurar Kimi API (Opcional)

Para capacidades avanzadas con Kimi AI:

```bash
export KIMI_API_KEY='your-api-key-here'
python3 medex_chat.py
```

Sin API key, MedeX funciona en modo demo con todas las capacidades locales.

### Estructura de Archivos

```
MedeX/
├── medex_chat.py          # Interfaz principal
├── core/
│   └── ai_engine.py       # Motor de IA médica
├── docs/
│   └── user_guide.md      # Esta guía
└── requirements.txt       # Dependencias
```

## 🆘 Soporte y Solución de Problemas

### Problemas Comunes

**❓ El sistema no detecta el tipo de usuario correctamente**
- Usa vocabulario más específico (médico vs personal)
- Ejemplos: "paciente presenta..." vs "me duele..."

**❓ No encuentra información médica relevante**
- Usa términos médicos específicos
- Incluye más contexto en la consulta

**❓ Error al ejecutar**
- Verifica instalación: `pip install -r requirements.txt`
- Comprueba versión Python >= 3.8

### Contacto

Para soporte técnico o mejoras al sistema, contacte al equipo de desarrollo.

---

**🏥 MedeX - Su asistente de IA médica inteligente**
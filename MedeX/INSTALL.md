# 🏥 MedeX - Guía de Instalación

## 🎯 **SISTEMA MÉDICO INTELIGENTE - LISTO PARA USAR**

**MedeX** está completamente configurado y listo para proporcionar asistencia médica inteligente.

---

## 🚀 **EJECUTAR MedeX (SIMPLE)**

### **Una sola línea de comando:**

```bash
cd /home/deeprat2/Escritorio/MedeX && python3 medex_chat.py
```

¡Y listo! MedeX se iniciará automáticamente.

---

## 💡 **CÓMO USAR MedeX**

### **1. Para Pacientes (Automático)**
Solo hable naturalmente:
```
"Me duele el pecho desde hace 2 horas"
"Tengo fiebre y me siento mal"
"¿Debo ir al doctor?"
```

### **2. Para Profesionales Médicos (Automático)**
Use lenguaje médico:
```
"Paciente 65 años, diabético, dolor precordial 2h"
"Protocolo manejo síndrome coronario agudo"
"Dosis aspirina en emergencia cardiovascular"
```

### **3. Comandos Especiales**
```
"demo paciente"     - Ver ejemplo paciente
"demo pro"          - Ver ejemplo profesional  
"estado"            - Ver estado del sistema
"estadísticas"      - Ver estadísticas sesión
"salir"             - Terminar
```

---

## 🧠 **LO QUE HACE MedeX AUTOMÁTICAMENTE**

### ✅ **Detección Inteligente**
- **Identifica** si eres paciente o médico
- **Adapta** el lenguaje automáticamente
- **Personaliza** las respuestas

### ✅ **Emergencias Médicas**
- **Detecta** emergencias automáticamente
- **Activa** protocolos de seguridad
- **Proporciona** instrucciones apropiadas

### ✅ **Conocimiento Médico Real**
- **Busca** en base de datos médica
- **Incluye** códigos ICD-10
- **Proporciona** información actualizada

---

## 📊 **EJEMPLO DE USO REAL**

```bash
cd /home/deeprat2/Escritorio/MedeX
python3 medex_chat.py

# El sistema se inicia...
🏥 MedeX Sistema Médico Iniciado

🩺 MedeX: Me duele el pecho

# MedeX detecta automáticamente:
👤 Usuario: PACIENTE
🚨 Urgencia: EMERGENCIA
📋 Respuesta adaptada para paciente...
```

---

## 🔧 **CONFIGURACIÓN OPCIONAL**

### **Para capacidades avanzadas con Kimi:**
```bash
export KIMI_API_KEY='tu-api-key'
cd /home/deeprat2/Escritorio/MedeX
python3 medex_chat.py
```

**Sin API key funciona perfectamente** en modo local.

---

## 📁 **ESTRUCTURA DEL PROYECTO**

```
/home/deeprat2/Escritorio/MedeX/
├── medex_chat.py          ← ARCHIVO PRINCIPAL
├── core/
│   └── ai_engine.py       ← Motor de IA médica
├── docs/
│   ├── user_guide.md      ← Guía detallada
│   └── ...
├── data/                  ← Datos médicos
├── requirements.txt       ← Dependencias
└── setup.py              ← Instalación automática
```

---

## ⚠️ **INFORMACIÓN MÉDICA IMPORTANTE**

### **✅ QUÉ HACE MedeX:**
- Proporciona información médica educativa
- Orienta sobre cuándo buscar ayuda
- Detecta emergencias y recomienda acción
- Adapta respuestas al nivel del usuario

### **❌ QUÉ NO HACE MedeX:**
- NO reemplaza al médico
- NO da diagnósticos definitivos  
- NO prescribe medicamentos
- NO toma decisiones médicas

### **🚨 EN EMERGENCIAS:**
**SIEMPRE llame al 911 primero**

---

## 🎉 **¡EMPEZAR AHORA!**

### **Comando único para ejecutar:**

```bash
cd /home/deeprat2/Escritorio/MedeX && python3 medex_chat.py
```

### **Pruebe con:**
- `"Me duele la cabeza"` (paciente)
- `"Paciente con cefalea"` (profesional)
- `"demo paciente"` (demostración)

---

**🏥 MedeX - Su asistente médico inteligente está listo**
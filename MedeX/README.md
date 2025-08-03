# 🏥 MedeX - Medical AI Intelligence System

## 🎯 Descripción del Proyecto

**MedeX** es un sistema de inteligencia artificial médica completo que combina conocimiento médico profesional con capacidades de IA multimodal para proporcionar apoyo diagnóstico y educativo tanto a profesionales de la salud como a pacientes.

## ✨ Características Principales

### 🧠 Inteligencia Médica Avanzada
- **Detección automática** de tipo de usuario (paciente vs profesional)
- **Análisis de contexto médico** inteligente
- **Respuestas adaptadas** según el nivel de conocimiento del usuario
- **Detección de emergencias** automática con protocolos apropiados

### 📚 Base de Conocimientos Médicos
- **Condiciones médicas** con códigos ICD-10
- **Información farmacológica** actualizada
- **Protocolos clínicos** basados en guías internacionales
- **Búsqueda semántica** en conocimiento médico

### 🔬 Capacidades Multimodales
- **Análisis de texto** médico avanzado
- **Procesamiento de imágenes** médicas (preparado para Kimi Vision)
- **Interpretación de estudios** complementarios
- **Documentación médica** automatizada

### 🛡️ Seguridad Médica
- **Disclaimers médicos** profesionales obligatorios
- **Protocolos de emergencia** automatizados
- **Derivación apropiada** a profesionales
- **Estándares de calidad** médica

## 🚀 Inicio Rápido

### Instalación
```bash
cd /home/deeprat2/Escritorio/MedeX
pip install -r requirements.txt
```

### Ejecución
```bash
# Chat médico interactivo
python3 medex_chat.py

# Análisis de documentos médicos
python3 medex_docs.py

# Análisis de imágenes médicas
python3 medex_imaging.py

# Monitoreo de pacientes
python3 medex_monitoring.py
```

## 📋 Casos de Uso

### 👨‍⚕️ Para Profesionales Médicos
- Apoyo diagnóstico con diagnósticos diferenciales
- Protocolos clínicos específicos
- Información farmacológica detallada
- Documentación médica automatizada

### 👤 Para Pacientes
- Educación médica comprensible
- Orientación sobre cuándo buscar atención
- Información sobre condiciones comunes
- Guías de autocuidado seguro

### 🏥 Para Instituciones
- Monitoreo de pacientes en tiempo real
- Análisis de imágenes médicas
- Documentación médica estandarizada
- Sistemas de alerta temprana

## 🏗️ Arquitectura del Sistema

```
MedeX/
├── medex_chat.py              # Interfaz principal de chat médico
├── core/                      # Núcleo del sistema
│   ├── ai_engine.py          # Motor de IA médica
│   ├── medical_knowledge.py  # Base de conocimientos
│   ├── context_analyzer.py   # Analizador de contexto
│   └── safety_protocols.py   # Protocolos de seguridad
├── modules/                   # Módulos especializados
│   ├── documentation/        # Documentación médica
│   ├── imaging/             # Análisis de imágenes
│   ├── monitoring/          # Monitoreo de pacientes
│   └── knowledge/           # Gestión de conocimiento
├── data/                     # Datos del sistema
│   ├── medical_conditions/  # Condiciones médicas
│   ├── medications/         # Base de datos de medicamentos
│   └── protocols/           # Protocolos clínicos
├── tests/                    # Suite de pruebas
├── docs/                     # Documentación
└── examples/                 # Ejemplos de uso
```

## 🧪 Testing

```bash
# Ejecutar todas las pruebas
python3 -m pytest tests/

# Validación del sistema médico
python3 tests/medical_validation.py

# Pruebas de seguridad
python3 tests/safety_tests.py
```

## 📖 Documentación

- [Guía de Usuario](docs/user_guide.md)
- [Documentación Técnica](docs/technical_docs.md)
- [Protocolos Médicos](docs/medical_protocols.md)
- [API Reference](docs/api_reference.md)

## ⚠️ Disclaimer Médico

**MedeX es un sistema de apoyo educativo y clínico únicamente.**

- ❌ NO reemplaza la evaluación médica profesional
- ❌ NO debe usarse como única fuente diagnóstica
- ✅ Proporciona información basada en evidencia
- ✅ Incluye protocolos de seguridad médica
- 🚨 En emergencias, contacte servicios de urgencia (911)

## 📄 Licencia

Este proyecto está bajo la Licencia MIT para uso educativo y de investigación.

## 👥 Contribuciones

Las contribuciones son bienvenidas. Por favor, lea nuestras guías de contribución y asegúrese de que todas las adiciones mantengan los estándares de seguridad médica.

## 📞 Soporte

Para soporte técnico o consultas sobre el sistema, contacte al equipo de desarrollo.

---

**🏥 MedeX - Medicina + AI = Futuro de la Atención Médica**
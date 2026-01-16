transcription-app/
├── .github/
│   └── workflows/
│       ├── test.yml          # Run tests on every push
│       ├── build.yml         # Build app on release
│       └── release.yml       # Create releases
├── electron/
│   ├── src/
│   ├── package.json
│   └── tsconfig.json
├── python/
│   ├── transcription_service.py
│   ├── requirements.txt
│   └── tests/
│       └── test_transcription.py
├── .gitignore
└── README.md
module.exports = {
  parserPreset: {
    parserOpts: {
      headerPattern: /^((?:of|ofscm)-\d+):?\s+(.+)$/i,
      headerCorrespondence: ['ticket', 'subject']
    }
  },
  rules: {
    'header-min-length': [2, 'always', 15],
    'header-max-length': [2, 'always', 150],
  },
  plugins: [
    {
      rules: {
        'ticket-format': (parsed) => {
          const { header } = parsed;
          const pattern = /^(of-\d+|ofscm-\d+):?\s+.{10,}$/i;

          if (!pattern.test(header)) {
            return [
              false,
              `Commit message must match format: <TICKET-ID> <subject> or <TICKET-ID>: <subject>

Examples:
  ✓ OF-1234 add user authentication feature
  ✓ OF-1234: add user authentication feature
  ✓ of-1234 add user authentication feature


Rules:
  - Must start with OF-XXX or OFSCM-XXX (case-insensitive)
  - Subject must be at least 10 characters`
            ];
          }
          return [true];
        }
      }
    }
  ],
  rules: {
    'ticket-format': [2, 'always'],
    'header-max-length': [2, 'always', 150],
  }
};

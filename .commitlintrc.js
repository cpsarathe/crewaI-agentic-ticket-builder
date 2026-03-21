module.exports = {
  extends: [],
  rules: {
    'ticket-format': [2, 'always'],
  },
  plugins: [
    {
      rules: {
        'ticket-format': ({ raw }) => {
          const ticketPattern = /^OF-\d{4}\s+.+/;
          const isValid = ticketPattern.test(raw);
          return [
            isValid,
            'Commit message must start with "OF-XXXX " followed by description (e.g., "OF-1234 add feature")'
          ];
        },
      },
    },
  ],
};
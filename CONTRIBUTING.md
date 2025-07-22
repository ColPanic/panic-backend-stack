# Contributing to AI Backend Services Stack

We love your input! We want to make contributing to the AI Backend Services Stack as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## Development Process

We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

### Pull Requests

1. Fork the repo and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes.
5. Make sure your code lints.
6. Issue that pull request!

### Local Development

```bash
# Clone your fork
git clone https://github.com/your-username/ai-backend-stack.git
cd ai-backend-stack

# Setup development environment
make setup

# Start services
make up

# Make your changes...

# Test your changes
make health
make test  # when tests are available

# Clean up
make down
```

## Any Contributions You Make Will Be Under the MIT Software License

In short, when you submit code changes, your submissions are understood to be under the same [MIT License](LICENSE) that covers the project.

## Report Bugs Using GitHub Issues

We use GitHub issues to track public bugs. Report a bug by [opening a new issue](https://github.com/your-org/ai-backend-stack/issues).

**Great Bug Reports** tend to have:

- A quick summary and/or background
- Steps to reproduce
  - Be specific!
  - Give sample code if you can
- What you expected would happen
- What actually happens
- Notes (possibly including why you think this might be happening, or stuff you tried that didn't work)

## Feature Requests

We welcome feature requests! Please:

1. Check if the feature already exists or is planned
2. Open an issue with the `enhancement` label
3. Clearly describe the feature and its use case
4. Consider if it fits the project's scope

## Coding Style

- Use clear, descriptive variable and function names
- Comment your code where necessary
- Follow Docker and Docker Compose best practices
- Keep configurations simple and well-documented
- Ensure compatibility across different environments

### Docker Compose Guidelines

- Use environment variables for configuration
- Include health checks for all services
- Set appropriate resource limits
- Use meaningful service names
- Include restart policies

### Makefile Guidelines

- Keep commands simple and intuitive
- Include help text for all commands
- Use consistent naming conventions
- Group related commands together

## Documentation

- Update README.md for user-facing changes
- Update DEPLOYMENT.md for deployment-related changes
- Include inline documentation for complex configurations
- Provide examples for new features

## Testing

Currently, testing is manual using the provided health checks and commands. We welcome contributions to add automated testing:

- Service health tests
- Integration tests
- Performance tests
- Security tests

## Community Guidelines

- Be respectful and inclusive
- Help others learn and grow
- Share knowledge and best practices
- Provide constructive feedback

## Questions?

Don't hesitate to ask questions! You can:

- Open a discussion on GitHub
- Join our community chat (if available)
- Tag maintainers in issues

Thank you for contributing! 🎉
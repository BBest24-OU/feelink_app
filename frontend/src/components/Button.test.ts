/**
 * Unit tests for Button component
 */
import { render, fireEvent } from '@testing-library/svelte';
import { describe, it, expect, vi } from 'vitest';
import Button from './Button.svelte';

describe('Button Component', () => {
  it('renders with default props', () => {
    const { getByRole } = render(Button);
    const button = getByRole('button');

    expect(button).toBeTruthy();
    expect(button).toHaveClass('btn');
  });

  it('renders with custom text', () => {
    const { getByText } = render(Button, { props: { default: 'Click Me' } });

    expect(getByText('Click Me')).toBeTruthy();
  });

  it('renders with primary variant', () => {
    const { getByRole } = render(Button, { props: { variant: 'primary' } });
    const button = getByRole('button');

    expect(button).toHaveClass('btn-primary');
  });

  it('renders with secondary variant', () => {
    const { getByRole } = render(Button, { props: { variant: 'secondary' } });
    const button = getByRole('button');

    expect(button).toHaveClass('btn-secondary');
  });

  it('renders with danger variant', () => {
    const { getByRole } = render(Button, { props: { variant: 'danger' } });
    const button = getByRole('button');

    expect(button).toHaveClass('btn-danger');
  });

  it('applies disabled state', () => {
    const { getByRole } = render(Button, { props: { disabled: true } });
    const button = getByRole('button');

    expect(button).toBeDisabled();
  });

  it('handles click events', async () => {
    const handleClick = vi.fn();
    const { getByRole, component } = render(Button);
    const button = getByRole('button');

    component.$on('click', handleClick);
    await fireEvent.click(button);

    expect(handleClick).toHaveBeenCalledOnce();
  });

  it('does not trigger click when disabled', async () => {
    const handleClick = vi.fn();
    const { getByRole, component } = render(Button, { props: { disabled: true } });
    const button = getByRole('button');

    component.$on('click', handleClick);
    await fireEvent.click(button);

    // Disabled buttons don't fire click events
    expect(handleClick).not.toHaveBeenCalled();
  });

  it('applies full width class', () => {
    const { getByRole } = render(Button, { props: { fullWidth: true } });
    const button = getByRole('button');

    expect(button).toHaveClass('w-full');
  });

  it('renders with small size', () => {
    const { getByRole } = render(Button, { props: { size: 'sm' } });
    const button = getByRole('button');

    expect(button).toHaveClass('btn-sm');
  });

  it('renders with large size', () => {
    const { getByRole } = render(Button, { props: { size: 'lg' } });
    const button = getByRole('button');

    expect(button).toHaveClass('btn-lg');
  });
});

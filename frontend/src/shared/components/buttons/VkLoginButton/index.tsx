import VkIcon from "./assets/vk.svg";

export const VKButton = () => {
  const host = window.location.origin;
  const cbLink = `${host}/login`;

  const onClick = () => {
    window.location.href = `https://oauth.vk.com/authorize?client_id=${
      import.meta.env.VITE_CLIENT_ID
    }&display=page&redirect_uri=${cbLink}&scope=270338&response_type=code&v=5.131`;
  };

  return (
    <button
      type="button"
      className="flex items-center gap-2 w-full border rounded-md h-9 justify-center hover:bg-slate-50"
      onClick={onClick}>
      <div className="w-5 h-5 flex items-center">
        <VkIcon />
      </div>
      <p className="text-slate-500 text-sm leading-4 font-medium">Войти через ВКонтакте</p>
    </button>
  );
};

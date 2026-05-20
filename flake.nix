{
  description = "ED HIS — Emergency Department Hospital Information System";
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };
  outputs = { self, nixpkgs }: let
    system = "x86_64-linux";
    pkgs = import nixpkgs { inherit system; };
    pythonEnv = pkgs.python3.withPackages (ps: with ps; [
      streamlit
      pymysql
      bcrypt
      python-dotenv
      pandas
    ]);
  in {
    devShells.${system}.default = pkgs.mkShell {
      packages = [ pythonEnv ];
      shellHook = ''
        echo "🏥 ED HIS Dev Shell"
        echo "Run: streamlit run app/app.py"
        echo ""
      '';
    };
  };
}
